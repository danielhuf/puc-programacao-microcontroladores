/* meArm library York Hack Space May 2014
 * A simple control library for Phenoptix' meArm
 * Usage:
 *   meArm arm;
 *   arm.begin(1, 10, 9, 6);
 *   arm.openGripper();
 *   arm.gotoPoint(-80, 100, 140);
 *   arm.closeGripper();
 *   arm.gotoPoint(70, 200, 10);
 *   arm.openGripper();
 */
#include <Arduino.h>
#include "ik.h"
#include "meArm.h"
#include <Servo.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define BASE_SIZE 40
#define Z_INDICATOR_MARGIN 2
#define Z_INDICATOR_WIDTH 4
#define GRIPPER_LENGTH 10
#define ARM_X_REACH 150
#define ARM_Y_REACH 200
#define ARM_MIN_Z -30
#define ARM_MAX_Z 100
#define REFRESH_RATE 100 // ms

const int Z_INDICATOR_HEIGHT = SCREEN_WIDTH - Z_INDICATOR_MARGIN * 2;
const int BASE_MARGIN = (SCREEN_HEIGHT - BASE_SIZE - Z_INDICATOR_MARGIN * 2 - Z_INDICATOR_WIDTH) / 2;
const int BASE_X = SCREEN_WIDTH - BASE_SIZE - BASE_MARGIN;
const int BASE_Y = BASE_MARGIN;
const int BASE_X_CENTER = BASE_X + BASE_SIZE / 2;
const int BASE_Y_CENTER = BASE_Y + BASE_SIZE / 2;

const float BX = BASE_X_CENTER;
const float AX = - float(BX - GRIPPER_LENGTH) / ARM_Y_REACH;

const float BY = BASE_Y_CENTER;
const float AY = - float(BY - GRIPPER_LENGTH) / ARM_X_REACH;

unsigned long previousRefresh = 0;


// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


bool setup_servo (ServoInfo& svo, const int n_min, const int n_max,
                  const float a_min, const float a_max)
{
    float n_range = n_max - n_min;
    float a_range = a_max - a_min;

    // Must have a non-zero angle range
    if(a_range == 0) return false;

    // Calculate gain and zero
    svo.gain = n_range / a_range;
    svo.zero = n_min - svo.gain * a_min;

    // Set limits
    svo.n_min = n_min;
    svo.n_max = n_max;

    return true;
}

int angle2pwm (const ServoInfo& svo, const float angle)
{
    float pwm = 0.5f + svo.zero + svo.gain * angle;
    return int(pwm);
}

//Full constructor with calibration data
meArm::meArm(int sweepMinBase, int sweepMaxBase, float angleMinBase, float angleMaxBase,
          int sweepMinShoulder, int sweepMaxShoulder, float angleMinShoulder, float angleMaxShoulder,
          int sweepMinElbow, int sweepMaxElbow, float angleMinElbow, float angleMaxElbow,
          int sweepMinGripper, int sweepMaxGripper, float angleMinGripper, float angleMaxGripper) {
  //calroutine();
  setup_servo(_svoBase, sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase);
  setup_servo(_svoShoulder, sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder);
  setup_servo(_svoElbow, sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow);
  setup_servo(_svoGripper, sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper);
}

void meArm::begin(int pinBase, int pinShoulder, int pinElbow, int pinGripper) {
  _pinBase = pinBase;
  _pinShoulder = pinShoulder;
  _pinElbow = pinElbow;
  _pinGripper = pinGripper;
  _base.attach(_pinBase);
  _shoulder.attach(_pinShoulder);
  _elbow.attach(_pinElbow);
  _gripper.attach(_pinGripper, 1000, 2000);
  
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.display();
  delay(2000);
  display.clearDisplay();
  display.display();

  //goDirectlyTo(0, 100, 50);
  goDirectlyToCylinder(0, 100, 50);
  openGripper();
}

void meArm::end() {
  _base.detach();
  _shoulder.detach();
  _elbow.detach();
  _gripper.detach();
}

//Set servos to reach a certain point directly without caring how we get there 
void meArm::goDirectlyTo(float x, float y, float z) {
  float radBase,radShoulder,radElbow;
  if (solve(x, y, z, radBase, radShoulder, radElbow)) {
    _base.write(angle2pwm(_svoBase,radBase));
    _shoulder.write(angle2pwm(_svoShoulder,radShoulder));
    _elbow.write(angle2pwm(_svoElbow,radElbow));
    _x = x; _y = y; _z = z;
    
    
    if (millis() > previousRefresh + REFRESH_RATE &&
        (_previousX != x || _previousY != y || _previousZ != z)) {
      redraw();
      
      previousRefresh = millis();
    }
    
    _previousX = x;
    _previousY = y;
    _previousZ = z;
  }    
}

//Travel smoothly from current point to another point
void meArm::gotoPoint(float x, float y, float z) {
  //Starting points - current pos
  float x0 = _x; 
  float y0 = _y; 
  float z0 = _z;
  float dist = sqrt((x0-x)*(x0-x)+(y0-y)*(y0-y)+(z0-z)*(z0-z));
  int step = 10;
  for (int i = 0; i<dist; i+= step) {
    goDirectlyTo(x0 + (x-x0)*i/dist, y0 + (y-y0) * i/dist, z0 + (z-z0) * i/dist);
    delay(50);
  }
  goDirectlyTo(x, y, z);
  redraw();
  delay(50);
}

void meArm::redraw(){
  display.clearDisplay();
  drawBase();
  drawArm();
  drawGripper();
  drawZIndicator();
  display.display();
}

void meArm::drawBase(){
  display.drawRect(BASE_X, BASE_Y, BASE_SIZE, BASE_SIZE, SSD1306_WHITE);
}

void meArm::drawArm(){
  int screenX = _y * AX + BX;
  int screenY = _x * AY + BY;
  
  display.drawLine(BASE_X_CENTER, BASE_Y_CENTER, screenX, screenY, SSD1306_WHITE);
}

void meArm::drawGripper(){
  int screenX = _y * AX + BX;
  int screenY = _x * AY + BY;
  
  float armAngle = atan2f(screenY - BASE_Y_CENTER, screenX - BASE_X_CENTER);
  float angleRightGripper = _isGripperOpened ? armAngle + M_PI_4 : armAngle + M_PI/16;
  float angleLeftGripper = _isGripperOpened ? armAngle - M_PI_4 : armAngle - M_PI/16;
  
  display.drawLine(screenX, screenY, screenX + cosf(angleRightGripper) * GRIPPER_LENGTH, screenY + sinf(angleRightGripper) * GRIPPER_LENGTH, SSD1306_WHITE);
  display.drawLine(screenX, screenY, screenX + cosf(angleLeftGripper) * GRIPPER_LENGTH, screenY + sinf(angleLeftGripper) * GRIPPER_LENGTH, SSD1306_WHITE);
}

void meArm::drawZIndicator(){
  int x = Z_INDICATOR_MARGIN;
  int y = SCREEN_HEIGHT - Z_INDICATOR_MARGIN - Z_INDICATOR_WIDTH;
  
  int z = constrain(_z, ARM_MIN_Z, ARM_MAX_Z);
  int barLength = (z - ARM_MIN_Z) * Z_INDICATOR_HEIGHT / (ARM_MAX_Z - ARM_MIN_Z);
  
  display.fillRect(x + Z_INDICATOR_HEIGHT - barLength, y, barLength, Z_INDICATOR_WIDTH, SSD1306_WHITE);
  display.drawRect(x, y, Z_INDICATOR_HEIGHT, Z_INDICATOR_WIDTH, SSD1306_WHITE);
}

//Get x and y from theta and r
void meArm::polarToCartesian(float theta, float r, float& x, float& y){
    _r = r;
    _t = theta;
    x = r*sin(theta);
    y = r*cos(theta);
}

//Same as above but for cylindrical polar coodrinates
void meArm::gotoPointCylinder(float theta, float r, float z){
    float x, y;
    polarToCartesian(theta, r, x, y);
    gotoPoint(x,y,z);
}

void meArm::goDirectlyToCylinder(float theta, float r, float z){
    float x, y;
    polarToCartesian(theta, r, x, y);
    goDirectlyTo(x,y,z);
}

//Check to see if possible
bool meArm::isReachable(float x, float y, float z) {
  float radBase,radShoulder,radElbow;
  return (solve(x, y, z, radBase, radShoulder, radElbow));
}

//Grab something
void meArm::openGripper() {
  _gripper.write(angle2pwm(_svoGripper,pi/2));
  if(!_isGripperOpened) {
    _isGripperOpened = true;
    redraw();
  }
  delay(300);
}

//Let go of something
void meArm::closeGripper() {
  _gripper.write(angle2pwm(_svoGripper,0));
  if(_isGripperOpened) {
    _isGripperOpened = false;
    redraw();
  }
  delay(300);
}

//Current x, y and z
float meArm::getX() {
  return _x;
}
float meArm::getY() {
  return _y;
}
float meArm::getZ() {
  return _z;
}


float meArm::getR() {
  return _r;
}
float meArm::getTheta() {
  return _t;
}
