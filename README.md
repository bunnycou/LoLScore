# LoLScore
## Display Ranked Leauge of Legends Wins and Losses in an OBS Browser source

You can host this app yourself or you can use my online hosted version (lolscore.carrotbyte.net)

Just add the following link as an OBS browser source!

`http://lolscore.carrotbyte.net/<region>/<username>/<tag>`

You can add /kd to the end to also display K/D

`http://lolscore.carrotbyte.net/<region>/<username>/<tag>/kd`

Should support all regions across Americas, Europe, and Asia

Supports all region values. When in doubt it can be easier to use `na`, `eu`, `asia`, or `sea`; for your region input based on your major region. 

Example for Doublelift since he, at the time of making, is streaming daily to reach challenger, so this page will usually display some information as long as he is streaming or streamed recently

`http://lolscore.carrotbyte.net/na/doublelift/na1/kd`

### Why LoLScore over alternatives like Lobobot?
LoLScore is 100% free with no watermarks and extremely easy to use, absolutely zero extra input or setup apart from entering a URL into an obs browser source. 
LoLScore can also be customized how **you** want it to be customized as long as you can handle a little css input. Just modify the OBS browser source custom css and modify the `p` tag. Here is an example of changing the text color.
![image](https://github.com/bunnycou/LoLScore/assets/35743816/163a1b92-b1ca-4d1d-8833-ad85a6d87a18)

*Formerly lolscore.cottoncarrot.net, the cottoncarrot url still works until June 2025*
