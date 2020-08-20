#include "CmdMessenger.h"

# define EN 8 // stepper motor enable, active low
# define X_DIR 5 // X -axis stepper motor direction control
# define Y_DIR 6 // Y -axis stepper motor direction control
# define Z_DIR 7 // Z -axis stepper motor direction control
# define X_STP 2 // X -axis stepper control
# define Y_STP 3 // Y -axis stepper control
# define Z_STP 4 // Z -axis stepper control

# define ENDSTOP_1 9
# define ENDSTOP_2 10

# define STEP_DELAY_1 10
# define STEP_DELAY_2 500

float value1, value2;
float motor_steps_1, motor_steps_2;
int motor_steps[2] = {0, 0};

CmdMessenger cmdMessenger = CmdMessenger(Serial, ',', ';', '/');

enum {
	motors,
	energize,
	deenergize,
  home_axis,
	motor_value_1,
	motor_value_2,
	energized,
  homed
};

void attach_callbacks(void) {
	cmdMessenger.attach(motors, do_move_motors);
	cmdMessenger.attach(energize, do_energize);
	cmdMessenger.attach(deenergize, do_deenergize);
	cmdMessenger.attach(home_axis, do_home);
}

void do_move_motors(void) {
	value1 = cmdMessenger.readBinArg<float>();
	value2 = cmdMessenger.readBinArg<float>();

	float motor_steps_1 = value1;
	float motor_steps_2 = value2;

	bool motor_dir_1 = true;
	bool motor_dir_2 = true;

	if (motor_steps_1 < 0) {
		motor_dir_1 = false;
		motor_steps_1 = -motor_steps_1;
	} else
		motor_dir_1 = true;

	if (motor_steps_2 < 0) {
		motor_dir_2 = false;
		motor_steps_2 = -motor_steps_2;
	} else
		motor_dir_2 = true;

	motor_steps[0] = motor_steps_1;
	motor_steps[1] = motor_steps_2;

	int total_steps = max(motor_steps_1, motor_steps_2);

	digitalWrite(X_DIR, motor_dir_1);
	digitalWrite(Y_DIR, motor_dir_2);

	for (int i = 0; i < total_steps; i++) {
		if (motor_steps[0] > 0) {
			digitalWrite(X_STP, HIGH);
			delayMicroseconds(STEP_DELAY_1);
			digitalWrite(X_STP, LOW);
			delayMicroseconds(STEP_DELAY_2);
			motor_steps[0] -= 1;
		}
		if (motor_steps[1] > 0) {
			digitalWrite(Y_STP, HIGH);
			delayMicroseconds(STEP_DELAY_1);
			digitalWrite(Y_STP, LOW);
			delayMicroseconds(STEP_DELAY_2);
			motor_steps[1] -= 1;
		}
	}

	cmdMessenger.sendBinCmd(motor_value_1, motor_steps_1);
	cmdMessenger.sendBinCmd(motor_value_2, motor_steps_2);
}

void do_energize(void) {
	digitalWrite(EN, LOW);
	cmdMessenger.sendCmd(energized, "True");
}

void do_deenergize(void) {
	digitalWrite(EN, HIGH);
	cmdMessenger.sendCmd(energized, "False");
}

void do_home() {
  bool is_homed = false;
  bool x_homed = false;
  bool y_homed = false;

  do {
    if (digitalRead(ENDSTOP_1) == 0) {
      x_homed = true;
    }

    if (digitalRead(ENDSTOP_2) == 0) {
      y_homed = true;
    }
    
    if (x_homed && y_homed) {
      is_homed = true;
    }
    
    delayMicroseconds(500);
	} while (is_homed == false);
 
  cmdMessenger.sendCmd(homed, is_homed);
}

void setup() {
	Serial.begin(115200);
	attach_callbacks();
	pinMode (X_DIR, OUTPUT); pinMode (X_STP, OUTPUT);
	pinMode (Y_DIR, OUTPUT); pinMode (Y_STP, OUTPUT);
	pinMode (Z_DIR, OUTPUT); pinMode (Z_STP, OUTPUT);

	pinMode(ENDSTOP_1, INPUT_PULLUP);
	pinMode(ENDSTOP_2, INPUT_PULLUP);

	pinMode (EN, OUTPUT);
	digitalWrite(EN, HIGH);
}

void loop() {
	cmdMessenger.feedinSerialData();
}
