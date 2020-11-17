import speedtest
import schedule
import time
import writer
import arguments

args = None

def run_test(source=None):
    try:
        if (source is not None):
            s = speedtest.Speedtest(source_address=source)
            filename = source
        else:
            s = speedtest.Speedtest()
            filename = 'default'
    except:
        return
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=False)
    writer.Writer(args.dir + filename + '.csv', s.results.dict()).log()
    

def speed_test():
    if args.src is None:
        run_test()
    else:
        for source in args.src:
            run_test(source=source)


def main():
    global args
    args = arguments.Arguments().validate()
    schedule.every(args.interval).minutes.do(speedtest)
    schedule.run_all(delay_seconds=0)
    if not args.exit:
        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == '__main__':
    main()
