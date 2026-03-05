#include <ignition/gazebo/System.hh>
#include <ignition/gazebo/Model.hh>
#include <ignition/gazebo/components/JointVelocityCmd.hh>
#include <ignition/gazebo/components/Joint.hh>
#include <ignition/gazebo/components/JointPosition.hh>
#include <ignition/gazebo/components/JointVelocity.hh>
#include <ignition/plugin/Register.hh>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <ignition/math/PID.hh>
#include <sdf/sdf.hh>
#include <vector>
#include <string>
#include <chrono>

namespace ignition
{
namespace gazebo
{
class LekiwiServoControlPlugin : public System,
                                 public ISystemConfigure,
                                 public ISystemUpdate
{
public:
  LekiwiServoControlPlugin() = default;

  void Configure(const Entity &_entity,
                 const std::shared_ptr<const sdf::Element> &_sdf,
                 EntityComponentManager &_ecm,
                 EventManager &/*_eventMgr*/) override
  {
    // Khởi tạo ROS 2
    if (!rclcpp::ok()) {
      rclcpp::init(0, nullptr);
    }
    node_ = rclcpp::Node::make_shared("lekiwi_servo_control");

    // Lấy model
    model_ = Model(_entity);

    // Lấy tham số từ SDF
    namespace_ = _sdf->Get<std::string>("robotNamespace", "/lekiwi").first;
    command_topic_ = _sdf->Get<std::string>("commandTopic", "arm_commands").first;
    joint_state_topic_ = _sdf->Get<std::string>("jointStateTopic", "joint_states").first;
    max_velocity_ = _sdf->Get<double>("maxVelocity", 5.236).first;

    // Lấy danh sách khớp và giới hạn góc
    if (_sdf->HasElement("joints")) {
      auto sdf_copy = _sdf->Clone(); // Sao chép để bỏ const
      sdf::ElementPtr joints_elem = sdf_copy->GetElement("joints");
      if (joints_elem->HasElement("joint")) {
        sdf::ElementPtr joint_elem = joints_elem->GetElement("joint");
        while (joint_elem) {
          std::string joint_name = joint_elem->Get<std::string>("name");
          double lower_limit = joint_elem->Get<double>("lowerLimit", -1.5708).first;
          double upper_limit = joint_elem->Get<double>("upperLimit", 1.5708).first;

          auto joint = model_.JointByName(_ecm, joint_name);
          if (joint != kNullEntity) {
            joints_.push_back(joint);
            joint_names_.push_back(joint_name);
            lower_limits_.push_back(lower_limit);
            upper_limits_.push_back(upper_limit);
            target_positions_.push_back(0.0);
            pids_.emplace_back(1.0, 0.1, 0.01); // PID: P=1.0, I=0.1, D=0.01
          } else {
            RCLCPP_ERROR(node_->get_logger(), "Không tìm thấy khớp %s", joint_name.c_str());
          }
          joint_elem = joint_elem->GetNextElement("joint");
        }
      }
    }

    if (joints_.empty()) {
      RCLCPP_ERROR(node_->get_logger(), "Không có khớp nào được chỉ định");
      return;
    }

    // Khởi tạo subscriber
    command_sub_ = node_->create_subscription<std_msgs::msg::Float64MultiArray>(
      namespace_ + "/" + command_topic_,
      10,
      std::bind(&LekiwiServoControlPlugin::OnCommand, this, std::placeholders::_1));

    // Khởi tạo publisher
    joint_state_pub_ = node_->create_publisher<sensor_msgs::msg::JointState>(
      namespace_ + "/" + joint_state_topic_, 10);

    RCLCPP_INFO(node_->get_logger(), "LekiwiServoControlPlugin đã được tải");
  }

  void Update(const UpdateInfo &_info, EntityComponentManager &_ecm) override
  {
    // Lấy khoảng thời gian
    double dt = std::chrono::duration<double>(_info.dt).count();
    if (dt <= 0) return;

    // Xuất bản trạng thái khớp
    sensor_msgs::msg::JointState joint_state;
    joint_state.header.stamp = node_->get_clock()->now();
    joint_state.name.resize(joints_.size());
    joint_state.position.resize(joints_.size());
    joint_state.velocity.resize(joints_.size());

    // Điều khiển từng khớp
    for (size_t i = 0; i < joints_.size(); ++i) {
      // Lấy vị trí và vận tốc hiện tại
      auto pos_comp = _ecm.Component<components::JointPosition>(joints_[i]);
      auto vel_comp = _ecm.Component<components::JointVelocity>(joints_[i]);
      double current_pos = pos_comp && !pos_comp->Data().empty() ? pos_comp->Data()[0] : 0.0;
      double current_vel = vel_comp && !vel_comp->Data().empty() ? vel_comp->Data()[0] : 0.0;

      // Tính lỗi và vận tốc điều khiển
      double error = target_positions_[i] - current_pos;
      double cmd_vel = pids_[i].Update(error, std::chrono::duration<double>(dt));

      // Giới hạn vận tốc
      cmd_vel = std::max(-max_velocity_, std::min(max_velocity_, cmd_vel));

      // Áp dụng vận tốc
      _ecm.SetComponentData<components::JointVelocityCmd>(joints_[i], {cmd_vel});

      // Cập nhật trạng thái khớp
      joint_state.name[i] = joint_names_[i];
      joint_state.position[i] = current_pos;
      joint_state.velocity[i] = current_vel;
    }

    joint_state_pub_->publish(joint_state);

    // Xử lý các callback ROS 2
    rclcpp::spin_some(node_);
  }

private:
  void OnCommand(const std_msgs::msg::Float64MultiArray::SharedPtr msg)
  {
    if (msg->data.size() != joints_.size()) {
      RCLCPP_WARN(node_->get_logger(), "Nhận được %lu vị trí, cần %lu",
                  msg->data.size(), joints_.size());
      return;
    }

    // Cập nhật vị trí mục tiêu với giới hạn góc
    for (size_t i = 0; i < msg->data.size(); ++i) {
      target_positions_[i] = std::max(lower_limits_[i], std::min(upper_limits_[i], msg->data[i]));
    }
  }

  Model model_;
  std::vector<Entity> joints_;
  std::vector<std::string> joint_names_;
  std::vector<double> target_positions_;
  std::vector<double> lower_limits_;
  std::vector<double> upper_limits_;
  std::vector<ignition::math::PID> pids_;
  rclcpp::Node::SharedPtr node_;
  rclcpp::Subscription<std_msgs::msg::Float64MultiArray>::SharedPtr command_sub_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_state_pub_;
  std::string namespace_;
  std::string command_topic_;
  std::string joint_state_topic_;
  double max_velocity_;
};
}
}

IGNITION_ADD_PLUGIN(
  ignition::gazebo::LekiwiServoControlPlugin,
  ignition::gazebo::System,
  ignition::gazebo::LekiwiServoControlPlugin::ISystemConfigure,
  ignition::gazebo::LekiwiServoControlPlugin::ISystemUpdate
)

IGNITION_ADD_PLUGIN_ALIAS(ignition::gazebo::LekiwiServoControlPlugin, "lekiwi_servo_control")

