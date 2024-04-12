import ollama
import shodan_tools
import cisa_search
import datetime
print("""  ____      _                __        __    _       _     ____                      _ 
  / ___|   _| |__   ___ _ __  \ \      / /_ _| |_ ___| |__ |  _ \  ___   __ _  __   _/ |
 | |  | | | | '_ \ / _ \ '__|  \ \ /\ / / _` | __/ __| '_ \| | | |/ _ \ / _` | \ \ / / |
 | |__| |_| | |_) |  __/ |      \ V  V / (_| | || (__| | | | |_| | (_) | (_| |  \ V /| |
  \____\__, |_.__/ \___|_|       \_/\_/ \__,_|\__\___|_| |_|____/ \___/ \__, |   \_(_)_|
       |___/                                                            |___/           
Version 1.0 An open source AI+RAG Multi-model Learning Tool for Vulnerability Management
Creators: Rich Wickersham, Tom Bendien and Joe Carroll  

               ......                  ............. 
            .....;;...                ................ 
         .......;;;;;/mmmmmmmmmmmmmm\/.................. 
       ........;;;mmmmmmmmmmmmmmmmmmm..................... 
     .........;;m/;;;;\mmmmmm/;;;;;\m...................... 
  ..........;;;m;;mmmm;;mmmm;;mmmmm;;m...................... 
..........;;;;;mmmnnnmmmmmmmmmmnnnmmmm\.................... 
.........  ;;;;;n/#####\nmmmmn/#####\nmm\................. 
.......     ;;;;n##...##nmmmmn##...##nmmmm\............. 
....        ;;;n#.....|nmmmmn#.....#nmmmmm,l......... 
 ..          mmmn\.../nmmmmmmn\.../nmmmm,m,lll..... 
          /mmmmmmmmmmmmmmmmmmmmmmmmmmm,mmmm,llll.. 
      /mmmmmmmmmmmmmmmmmmmmmmm\nmmmn/mmmmmmm,lll/ 
   /mmmmm/..........\mmmmmmmmmmnnmnnmmmmmmmmm,ll 
  mmmmmm|...........|mmmmmmmmmmmmmmmmmmmmmmmm,ll 
  \mmmmmmm\......./mmmmmmmmmmmmmmmmmmmmmmmmm,llo 
    \mmmmmmm\.../mmmmmmmmmmmmmmmmmmmmmmmmmm,lloo 
      \mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm,ll/oooo 
         \mmmmmmmmmmll..;;;.;;;;;;/mmm,lll/oooooo\ 
                   ll..;;;.;;;;;;/llllll/ooooooooo 
                   ll.;;;.;;;;;/.llll/oooooooooo..o 
                   ll;;;.;;;;;;..ll/ooooooooooo...oo 
                   \;;;;.;;;;;..ll/ooooo...ooooo..oo\ 
                 ;;;;;;;;;;;;..ll|oooo.....oooooooooo 
                ;;;;;;.;;;;;;.ll/oooo.....ooooooo....\ 
                ;;;;;.;;;;;;;ll/ooooooooooooo.....oooo 
                 \;;;.;;;;;;/oooooooooooo.....oooooooo\ 
                  \;;;.;;;;/ooooooooo.....ooooooooooooo 
                    \;;;;/ooooooo.....ooooooooooo...ooo\ 
                    |o\;/oooo.....ooooooooooooo......ooo 
                    oooooo....ooooooooooooooooooo.....oo\ 
                   oooo....oooooooooooooooooooooooo..oooo 
                  ___.oooooooooooooo....ooooooooooooooooo\ 
                 /RAG\oooooooooooo.....ooooooooooooooooooo 
                 |AI|ooooo.oooooo....ooooooooooooooooooooo 
               /oo\ML/oooo..ooooooooooooooooooo..oooooooooooo 
 """)             
llm_model = 'llama2'

while True:
    fdtn = str((datetime.datetime.now().day)) + str((datetime.datetime.now().month)) + str((datetime.datetime.now().year)) + str((datetime.datetime.now().hour)) + str((datetime.datetime.now().minute)) + str((datetime.datetime.now().second))
    companyName = str(input('\nEnter company name: '))
    shodanReport = shodan_tools.shodan_org_scan(companyName)
    print('\nShodan Report:\n{0}\n\n'.format(shodanReport))
    fullReport = ''
    if len(shodanReport) > 0:
        stream = ollama.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': 'Here is a report from Shodan: {0} Provide a summary of this report. Then, detail steps of mitigation in bullet format'.format(shodanReport)}],
            stream=True,
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            fullReport = fullReport + chunk['message']['content']
        file = open("shodan_report_{0}.txt".format(fdtn), "a")
        file.write("\nSearch for: {0}".format(companyName))
        file.write("\n\n\n")
        file.write(shodanReport)
        file.write("\n\n\n")
        file.write(fullReport)
        file.close()
    else:
        print("Information not found.")
    print("Done!\n\n")
