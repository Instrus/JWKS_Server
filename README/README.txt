KNOWN ISSUES:
Gradebot is a bit sensitive.

Please refer to the example screenshot (known_issues_screenshot).

As you can see on different runs (not consecutive as the server was restarted for every test) I got different scores.

I have verified several times that the score I have achieved is 65. Gradebot, however, continues to cycle between 10, 45, 65, claiming timeout errors, or expired JWT not found.

If you are not seeing the score 65, please try running my program again, and run gradebot.

The issue seems to be from the fact I am using Python/Flask instead of Go.

If you are getting the error:
ERROR msg="/auth valid JWT authN" err="Post \"http://127.0.0.1:8080/auth\": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
run the program again. run gradebot.exe project1 again.

If you are getting errors related to expired JWT not found, try running again.

Thank you.