# termato
BUILT TO address my own problem:

https://psychology.stackexchange.com/questions/27694/the-perception-of-time-of-workaholics

People working on their laptops often forget the whole world while they're engrossed in their work. Some fall into compulsive habits or disorders, while others dislike installing complicated and overly colorful GUI nonsense. There are those who prefer minimalist tools that simply get the job done.

Basically, you know you need to get up and take a small break, but you convince yourself to finish "just one more thing," and before you know it, the entire day has slipped by. You’re still in front of your laptop or screen, trying to fix that one last thing. Sure, it’s rewarding, and I love that more than anything. But deep down, we know we need to take at least small breaks.

This program was built for me, but I don’t see why others wouldn’t find it useful too.

Why not simply buy a pomodoro? Well, I want my laptop to take care of me the way I do:)

# Pomodoro Timer Help
-------------------

![image](15-5-3.png)


## Install the package

```bash
pip install termato
pip3 install termato
```
## How to execute

```bash
$ termato
```
Or
```bash
$ termato -w=25 -b=5 -r=4
```
## Options

- **-w=<work_time>**: Set the duration of each work interval in minutes. Default: 25 minutes.
- **-b=<break_time>**: Set the duration of each regular break in minutes. Default: 5 minutes.
- **-r=<rounds>**: Set the total number of completed pomodoro intervals (work round + break). Default: 4.
- **-h**: Display this help message.


## Note

- The script will use default values if any option is not provided.
- Only `-w`, `-b`, `-r` options are recognized. All other parameters will be ignored.
- Press Ctrl+C during the timer to stop the script.

## License

This project is licensed under the Custom License. See the [LICENSE](./LICENSE) file for details.


## Future Versions, Bug, and Errors: 
Well, I’m sorry, but I don’t have time for anything like that. Besides, I personally don’t think this code deserves much attention because it’s just a simple script turned into a command line and found this old script somewhere on my old file archives