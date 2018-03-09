# simple_baseline_server
Simple Python Flask Server for two-class human classification.  
Works on mobile and can easily be hosted with nginx through wsgi.

## Installation
The default expects a sqlite database with a DATA table that contains an ID and a PK and CONTENT as a String.   
Results are written back into a BASELINE table, that contains ID(PK), CONTENTID(FK), ISPOSITIVE(BOOL), TIME(TIMESTAMP) and USER(STRING).

The only required package is Flask. Install via `pip3 install flask`

![](/screenshots/user_selection.png )  
![](/screenshots/evaluation.png)
