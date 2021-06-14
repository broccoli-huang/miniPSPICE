# MiniPSPICE

110下 臺大電機普物 期末專題 
by 戴瑋佑、黃元顥、楊博宇
---
## Video Link
[MiniPSPICE implemented by vPython](https://www.youtube.com/watch?v=FUu-BAtbR5g)

## GitHub Link
[miniPSPICE](https://github.com/broccoli-huang/miniPSPICE)

## How to Use
1. Create a text file that describe your circuit. 
(Some examples -- AC1.txt, AC2.txt, DC1.txt, DC2.txt, DC3.txt, DC4.txt -- are provided, you can use them directly!)
2. Put the file under the same directory as `parse.py`.
3. Run `parse.py`.
4. Enter your file name.
```Input File: {your file name}```
5. It will automatically generate the result and circuit diagram.

## Circuit Description Format

#### Naming Nodes
Please assign a unique name for each node. You can use single capital letters, i.e., A,B,C,... .

#### Comments
- Lines begin with `#` are comments.
```# This is comment.```
- Everything behind ` //` are comments in each line. (Please make sure there is a space between `//` and previous character.)
```V 12 A B // This is comment.```

#### Type of Circuit
Specify the circuit type (AC or DC) at the first non-comment line. Also describe the frequency (in Hz) for AC circuit by adding a space and the desired frequency after ```AC```.
- AC: `AC 123.4 // freq = 123.4 Hz`
- DC: `DC // no need to tell frequency`

#### Components
Each component is described by a single line. Their Order doesn't matter. 
There are some restrictions for components, please refer to the video for details. 
##### AC Voltage source
Note: Only accept single voltage source.
```V {magnitude in V} {phase in degree} {positive node} {negative node}```
E.g. `V 12 30 A D // Voltage source 12V <30, A+ D-`
##### DC Voltage source
```V {magnitude in V} {positive node} {negative node}```
E.g. `V 7 A F // Voltage source 7V, A+ F-`
##### Resistor
```R {value in Ohm} {node1} {node2}```
E.g. `R 2 A B // 2 Ohm resistor between A & B`
##### Inductor
```L {value in H} {node1} {node2}```
E.g. `L 0.002 A B // 2mH inductor between A & B`
##### Capacitor
```C {value in F} {node1} {node2}```
E.g. `C 0.001 A B // 1mF capacitor between A & B`

#### Node Order
You can specify display node order by adding this line at the end:
```& A B C D```
The nodes will be displayed in the order A B C D (from left to right). 

## Results
The result shows the circuit diagram, the voltage of each node, and the terminal voltage of each component (with + and - side shown).
Note that we can't display the "angle symbol" in vpython, so we use "<" instead.

## Error Handling
- `ERROR! Please specify AC or DC.` -- Please specify AC oe DC at the beginning.
- `ERROR! Node order unmatched.` -- The node order you specified doesn't match the name or number of nodes in the circuit. It can also be caused by some extra spacing in the line. Please make sure there is exactly one spacing between `&`, `{node-names}`, and `//`. For example, 
```& A B C D // Exactly one space between every element.```
- Other Error  -- Please check your input file format. 




