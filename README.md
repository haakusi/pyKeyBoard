# pyKeyBoard
Writing something? Summary all! Generate something!<br>
'pyKeyBoard' will be Records your computer input values by Keyboard typing.<br>
<br>
<br>

    1. Start 'pyKeyBoard' process, writting all by keyboard input.
    2. Press pattern or button(if makes gui).<br>
    3. Makes txt files, ex) pyKeyBoard_211229.txt<br> 
    4. Makes json format. ex) { "process_title": "[input, intput, input...]", "process_title": "[input, intput, input...]" }
    5. Summary analysis to json, makes summary result files(ex. txt...)<br>
       In this step, we can use to 'bart' models. it can be more efficenty others.. <-- *need to check other models and compare
    6. Finds 'KeyWords' in summaries and Makes sentences to use 'GPT' models.<br>
    
<br>
<br>

### Dev Story
<details markdown="1">
<summary>21.12.29 - *[Edit] README.md, *[Commit] main.py</summary>

    noti)
    - First commit in this project. maybe next times, bug fixed and dev somethings.

    fixed)
    - if i get to know about focus programs, i need to know about korean/english program status.. return
</details>

<br>
<br>

### Todo Dev List
    1. consider about : process unit.. get hanFlag..? thinking about more efficiency solutions....
    2. eng/kor status logic. if make 1 sentence -> write() : more efficiency than now..
    3. json data structure.. to use 'bart' models
    4. adjust special keys Shift, Ctrl.. key +@ : event type UP/DOWN to Check write only 1.
    5. space, shift, ctrl.. at least space, backspace, enter to adjust code by unicode
    6. need to exit sequence... function (now key press 'f1')
    7. next to makes .json format. english / korean checked.. maybe utf-8 > unicode? 
       this time checking utf8/unicode in korean. to used.. modules.. lib...
    8. interface. ~ing thread -> moving img..
    9. if saved completely, key, val += string -> need to convert 'json' preprocessing.
    10. backspace -> delete, pop[-1]
    11. key press 3,1times 'f10','f11' likes 'f10f10f10f11' -> To read testKeyBoard_%s.txt -> It makes to obj json [{ "key" : "val" }, { "key" : "val" }, ...]
    12. key press 3,1times 'f11','f12' likes 'f11f11f11f12' -> obj json -> to use pretrained bert Model.. -> output
    13. after preprocessing, adjust to BART, BERT.. to use content summary model

    ### orinary consider about this 'pyKeyBoard' project.
      and then another function likes bert, lstm..
      analysis that means.. 
      likes this..
      what can i do something with program, text... logs..
      ** idea) to use BERT -> summary(), and next to extract keyword, it can use to 1~2 sentence generation. (likes GPT) -- so fun, enjoying.
      ** serious safety) login page id/pw need.. blocked version
    
    

     

   

      

     