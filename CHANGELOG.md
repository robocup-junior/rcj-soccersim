# CHANGELOG

## Unreleased

* Features
  * **BREAKING** Change the message format sent between Emitter and Receiver
  * Update Webots from R2022a to R2023b
* Other
  * Update development requirements

## v2.1

* Features
  * **BREAKING** [#129](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/129) Set TIME STEP to 32 for robot controllers, ball and supervisor
* Refactoring
  * [#128](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/128) Move enums to enums.py
* Other
  * [#135](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/135) Rename soccer-sim to soccersim
  * [#133](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/133) Workaround for the relocation bug
    (so the robots won't fall over)

## v2.0

* Features
  * **BREAKING**: [#125](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/125) Update Webots to R2022a - 
    the coordinate system has changed
  * **BREAKING**: [#117](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/117) Add GPS, Compass and IR Ball sensors -
    robots do not get the exact position of the ball and other robots.
  * [#121](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/121) Add DistanceSensors of type sonar
  * [#90](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/90) Add inter-robot communication
* Refactoring
  * [#123](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/123) Add unittests
  * [#120](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/120) Split Referee and Supervisor
  * [#51](https://github.com/RoboCupJuniorTC/rcj-soccersim/pull/51) Add code style checkers and setup CI
* Other
  * Documentation updates

## v1.0

* Initial version