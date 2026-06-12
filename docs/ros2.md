# ROS2 Integration

`robot-experience-memory` provides optional ROS2 integration primitives under
`robot_experience_memory.ros2`. ROS2 is not a required dependency: importing the
main package and the ROS2 helper package works without `rclpy` installed.

## Optional dependency model

- Helpers use plain Python mappings, protocols, and duck typing where possible.
- `rclpy` is imported lazily only by explicit availability helpers.
- Calls that require real ROS2 raise `OptionalDependencyError` when `rclpy` is
  unavailable.
- Tests and non-ROS workflows can use fake publishers, fake lifecycle nodes, and
  generic request/response callbacks.

## Capture ROS-style executions

Use `ROS2ActionCapture` or `capture_action_execution` with an
`ExperienceRecorder` to store an action execution from a node, action server, or
robot script. Inputs are normal dictionaries so ROS message conversion can stay
at the application boundary.

## Publish outcomes and replay events

`publish_outcome`, `publish_recovery_suggestion`, and `publish_replay_event`
accept any object with a `publish(message)` method. By default they publish a
JSON string; callers can pass a message factory to create ROS message objects.

## Rosbag references

`RosbagReference` and `rosbag_sensor_reference` record lightweight rosbag
references as `SensorReference` metadata. They do not parse or validate rosbag
files.

## Lifecycle and services

Lifecycle helpers snapshot node-like objects with `get_name()`. Service helpers
wrap retrieval and recovery request handlers using caller-provided request
parsers and response builders, avoiding generated ROS service dependencies.

## Limitations

This integration layer does not command robots, create ROS nodes, spin
executors, parse bags, or define generated ROS messages. It is intentionally a
thin bridge between ROS2 applications and the framework-independent memory
library.
