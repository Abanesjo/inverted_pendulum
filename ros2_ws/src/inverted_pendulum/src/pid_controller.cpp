#include <gazebo/common/Plugin.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>

#include <iostream>
#include <string>
#include <time.h>
#include <sstream>
#include <Eigen/Dense>

#include "rclcpp/rclcpp.hpp"
#include "gazebo_ros/node.hpp"

#include <std_msgs/msg/float64.hpp>

namespace gazebo
{
class PIDController : public ModelPlugin
{
private:
    double cmd, integral, Kp, Kd, Ki;
    physics::JointPtr revolute, prismatic;
    physics::ModelPtr model;
    event::ConnectionPtr updateConnection;

public:
    double LIM_;
    rclcpp::Node::SharedPtr nh;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr force_feedback;

    void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
        nh = gazebo_ros::Node::Get(_sdf);
        this->model = _parent;
        this->cmd = 0.0;
        this->integral = 0.0;
        this->Kp = 4000;
        this->Kd = 400;

        std::string revolute_joint, prismatic_joint, ns;
        revolute_joint = _sdf->GetElement("revolute_joint")->Get<std::string>();
        prismatic_joint = _sdf->GetElement("prismatic_joint")->Get<std::string>();
        ns = _sdf->GetElement("namespace")->Get<std::string>();

        this->revolute = this->model->GetJoint(ns+"::"+revolute_joint);
        this->prismatic = this->model->GetJoint(ns+"::"+prismatic_joint);

        force_feedback = nh->create_publisher<std_msgs::msg::Float64>(ns+"/force", 1);

        this->updateConnection = event::Events::ConnectWorldUpdateBegin(std::bind(&PIDController::Update, this));
    }

    void Update()
    {
        double force = 0.0;
        double angle = this->revolute->Position(0);
        double rate = this->revolute->GetVelocity(0);

        force = -(this->Kp) * (angle - this->cmd) - Kd*rate;
        this->prismatic->SetForce(0, 1000000);

        std_msgs::msg::Float64 feedback_msg;
        feedback_msg.data = force;
        force_feedback->publish(feedback_msg);

        printf("HELLO_WORLD!\n");

        return;
    }


};
GZ_REGISTER_MODEL_PLUGIN(PIDController)
}