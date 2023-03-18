#ifndef STEPPER_H
#define STEPPER_H

#include "define.h"

class Stepper {

    enum class Direction { Forward, Backward };

    private:

    int steps_count = 0;

    int enable_pin, dir_pin, step_pin, boost_pin, fault_pin = -1;

    int step_duration_ms = 0;

    public:

    Stepper(int enable_pin, int dir_pin, int step_pin, int boost_pin, int fault_pin, int step_duration_ms):
        enable_pin(enable_pin),
        dir_pin(dir_pin),
        step_pin(step_pin),
        boost_pin(boost_pin),
        fault_pin(fault_pin),
        step_duration_ms(step_duration_ms) {

        pinMode(enable_pin,OUTPUT);
        pinMode(dir_pin,OUTPUT);
        pinMode(step_pin,OUTPUT);
        pinMode(boost_pin,OUTPUT);
        pinMode(fault_pin,INPUT_PULLUP);

        High(enable_pin);
    }

    ~Stepper(){
        
    }

    void step(int steps){

        Direction dir = Direction::Forward;

        if(steps < 0){
            steps = -steps;
            dir = Direction::Backward;
        }

        for(int i = 0; i < steps; i++){
            if(dir == Direction::Forward){
                step_forward();
            }
            else if (dir == Direction::Backward) {
                step_backward();
            }
        }
    }

    int get_steps_count(){
        return steps_count;
    }

    void step_forward(){

        High(dir_pin);

        High(step_pin);
        delay(step_duration_ms/2);
        Low(step_pin);
        delay(step_duration_ms/2);

        this->steps_count++;
    }

    void step_backward(){

        Low(dir_pin);

        High(step_pin);
        delay(step_duration_ms/2);
        Low(step_pin);
        delay(step_duration_ms/2);

        this->steps_count--;
    }

};

#endif