#include "CmdMessenger.h"

# define EN 8 // stepper motor enable, active low
# define A1_DIR 5 // a1 axis motor direction control
# define A2_DIR 6 // a2 axis motor direction control
# define A1_STP 2 // a1 axis motor step control
# define A2_STP 3 // a2 axis motor step control

# define ENDSTOP_A1 9
# define ENDSTOP_A2 10

# define STEP_DELAY_1 5
# define STEP_DELAY_2 600

float value1, value2;
float motor_steps_a1, motor_steps_a2;
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

	float motor_steps_a1 = value1;
	float motor_steps_a2 = value2;

	bool motor_dir_1 = true;
	bool motor_dir_2 = true;

	if (motor_steps_a1 < 0) {
		motor_dir_1 = false;
		motor_steps_a1 = -motor_steps_a1;
	} else
		motor_dir_1 = true;

	if (motor_steps_a2 < 0) {
		motor_dir_2 = false;
		motor_steps_a2 = -motor_steps_a2;
	} else
		motor_dir_2 = true;

	motor_steps[0] = motor_steps_a1;
	motor_steps[1] = motor_steps_a2;

	int total_steps = max(motor_steps_a1, motor_steps_a2);

	digitalWrite(A1_DIR, motor_dir_1);
	digitalWrite(A2_DIR, motor_dir_2);

	for (int i = 0; i < total_steps; i++) {
		if (motor_steps[0] > 0) {
			digitalWrite(A1_STP, HIGH);
			delayMicroseconds(STEP_DELAY_1);
			digitalWrite(A1_STP, LOW);
			delayMicroseconds(STEP_DELAY_2);
			motor_steps[0] -= 1;
		}
		if (motor_steps[1] > 0) {
			digitalWrite(A2_STP, HIGH);
			delayMicroseconds(STEP_DELAY_1);
			digitalWrite(A2_STP, LOW);
			delayMicroseconds(STEP_DELAY_2);
			motor_steps[1] -= 1;
		}
	}

	cmdMessenger.sendBinCmd(motor_value_1, motor_steps_a1);
	cmdMessenger.sendBinCmd(motor_value_2, motor_steps_a2);
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
  value1 = cmdMessenger.readBinArg<float>();
  value2 = cmdMessenger.readBinArg<float>();

  float home_offset_a1 = value1;
  float home_offset_a2 = value2;

	bool is_homed = false;
  bool a1_limit_hit = false;
  bool a2_limit_hit = false;
	bool a1_homed = false;
	bool a2_homed = false;

  digitalWrite(A1_DIR, true);
  digitalWrite(A2_DIR, false);

	while (is_homed == false) {

    // a1 hasn't hit limit? move motor X steps
    if (a1_limit_hit == false && a1_homed == false && a2_limit_hit == false && a2_homed == false) {
      for (int i = 0; i <= 10; i++) {
        digitalWrite(A1_STP, HIGH);
        delayMicroseconds(STEP_DELAY_1);
        digitalWrite(A1_STP, LOW);
        delayMicroseconds(STEP_DELAY_2);
      }

      if (digitalRead(ENDSTOP_A1) == 0) {
        a1_limit_hit = true;
      }
    }

    // a1 limit hit but not homed?
    if (a1_limit_hit == true && a1_homed == false && a2_limit_hit == false && a2_homed == false) {

      digitalWrite(A1_DIR, false);
      
      for (int i = 0; i <= home_offset_a1; i++) {
        digitalWrite(A1_STP, HIGH);
        delayMicroseconds(STEP_DELAY_1);
        digitalWrite(A1_STP, LOW);
        delayMicroseconds(STEP_DELAY_2);
      }

      a1_homed = true;
    }

    // a1 has homed but a2 has not.
    if (a1_limit_hit == true && a1_homed == true && a2_limit_hit == false && a2_homed == false) {
      for (int i = 0; i <= 10; i++) {
        digitalWrite(A2_STP, HIGH);
        delayMicroseconds(STEP_DELAY_1);
        digitalWrite(A2_STP, LOW);
        delayMicroseconds(STEP_DELAY_2);
      }
      
      if (digitalRead(ENDSTOP_A2) == 0) {
        a2_limit_hit = true;
      }
    }

    // a1 limit hit but not homed?
    if (a1_limit_hit == true && a1_homed == true && a2_limit_hit == true && a2_homed == false) {

      digitalWrite(A2_DIR, true);
      
      for (int i = 0; i <= home_offset_a2; i++) {
        digitalWrite(A2_STP, HIGH);
        delayMicroseconds(STEP_DELAY_1);
        digitalWrite(A2_STP, LOW);
        delayMicroseconds(STEP_DELAY_2);
      }

      a2_homed = true;
    }
    
		if (a1_homed == true && a2_homed == true) {
			is_homed = true;
		}
	}

	cmdMessenger.sendCmd(homed, is_homed);
}

void setup() {
	Serial.begin(115200);
	attach_callbacks();
	pinMode(A1_DIR, OUTPUT); pinMode(A1_STP, OUTPUT);
	pinMode(A2_DIR, OUTPUT); pinMode(A2_STP, OUTPUT);

	pinMode(ENDSTOP_A1, INPUT_PULLUP);
	pinMode(ENDSTOP_A2, INPUT_PULLUP);

	pinMode(EN, OUTPUT);
	digitalWrite(EN, HIGH);
}

void loop() {
	cmdMessenger.feedinSerialData();
}
