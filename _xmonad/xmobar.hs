Config { font = "-misc-fixed-*-*-*-*-18-*-*-*-*-*-*-*"
       , bgColor = "black"
       , fgColor = "grey"
       , position = BottomSize R 100 24
       , lowerOnStart = False
       , commands = [ Run MultiCpu ["-L","3","-H","50","-n","green","-h","red", "-t", "<autototal>%"] 50
                    , Run CpuFreq ["-t", "<cpu0>"] 50
                    , Run Memory ["-t","<usedratio>%"] 50
                    , Run Swap ["-t","<usedratio>%"] 50
                    , Run Date "%a %Y-%m-%d %H:%M" "date" 600
                    , Run Com "acpi" [] "" 1800
                    , Run StdinReader
                    ]
       , sepChar = "%"
       , alignSep = "}{"
       , template = "%StdinReader% }{ CPUs: %multicpu% @ %cpufreq% | Mem: %memory% * Swap: %swap% | %acpi% | %date%"
       }
