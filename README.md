# Analog-Electronics
Project for Analog Electronics I (ET3230) - SEEE - HUST: Audio Amplifier  
DESIGN FOR 1ST STAGE AND SIMULATION FOR ALL STAGE



## 1. To access design tool
   - Run python file: Notbypass.py
   - Circuit:<br>
         ![image](https://github.com/user-attachments/assets/65e173d7-2b34-44f7-a6b1-273d8cdd82ef)
   - INPUT:
       + Voltage supply:
       + Total voltage gain: Desize A_v or G you want
       + DC Current gain: hFE (or Beta) coefficient. I recommend to use Digital Multimeter to measure this coefficient.
   - OUTPUT:
       + R1 & R2 actual value must multiply by 10 (For lazy I've not modify in code)
       + Resistors' value has been normalized to standard value, so you can easily choose resistor to buy 
       + Precision: (Coefficient to evaluate Q_point is at the middle of DC Load Line or not) Near 100 is good
       + Gain: Actual gain calculate with normal resistors' value
       + Linear: If not Linear, please increase Voltage supply or decrease Total voltage gain
   - NOTE:
       + Actual value of resistor could vary from each components with same design value
   - Experience:
       + Increase R1 or reduce R2 -> Lower operating point (Q)
       + Increase RE or reduce RC -> Lower operating point (Q)

## 2. Simulation
   - Sim with Proteus (easy to use). If u want advance sim, LTSpice is recommend
   - Right Click and choose Root sheet 2. Or click to "Design" -> root sheet 2

