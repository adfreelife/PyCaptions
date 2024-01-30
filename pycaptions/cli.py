def main():
    import argparse
    import os

    from pycaptions.captions import Captions
    from pycaptions.captionsFormat import save_extensions
    from pycaptions.microTime import MicroTime as MT

    
    parser = argparse.ArgumentParser(prog='PyCaptions', description='Captions converter')
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("-f", "--format", nargs="+", default="all")
    parser.add_argument("-j", "--join", nargs="+", default="end_time")
    parser.add_argument("-tf", "--time-format", nargs="+", default="VTT")
    parser.add_argument("-l", "--languages", nargs="+")
    parser.add_argument("-o", "--out-filenames", nargs="+") 

    time_format = {
        "microtime": MT.fromMicrotime,
        "VTT": MT.fromVTTTime,
        "SRT": MT.fromSRTTime,
        "TTML": MT.parseTTMLTime,
        "SUB": MT.fromSUBTime
    }

    supported_extensions = save_extensions.getvars().values()
    args = parser.parse_args()

    formats = None
    languages = None

    if args.out_filenames:
        out_filenames = args.out_filenames
        if args.format == "all":
            formats = []
            for i in args.filenames:
                _, ext = os.path.splitext(i)[0] 
                if ext not in supported_extensions:
                    print(f"Incorect file format {ext} for {i}")
                    print(f"Supported extensions {supported_extensions}")
                    return -1
                formats.append(ext)

        languages = [Captions.getLanguagesFromFilename(i) or args.languages
                     for i in args.out_filenames]
            
    else:
        out_filenames = [os.path.splitext(i)[0] for i in args.filenames]

    if not formats:
        if args.format == "all":
            formats = [supported_extensions for _ in args.filenames]
        else:
            formats = [args.format for _ in args.filenames]

    if not languages:
        languages = [args.languages for _ in args.filenames]

    if not args.join:
        for _in, _out, _lang in zip(args.filenames, out_filenames, languages):
            with Captions(_in) as c:
                for out_format in formats:
                    c.save(_out, _lang, out_format)
    elif args.join == "end_time":
        with Captions(args.filenames[0]) as c:
            for next_file in args.filenames[1:]:
                c.join(Captions(next_file),True)
            for out_format in formats:
                c.save(out_filenames[0], languages[0], out_format)
    elif args.join == "add":
        with Captions(args.filenames[0]) as c:
            for next_file in args.filenames[1:]:
                c += Captions(next_file)
            for out_format in formats:
                c.save(out_filenames[0], languages[0], out_format)
    else:
        with Captions(args.filenames[0]) as c:
            for next_file, offset in zip(args.filenames[1:], args.join):
                c.join(Captions(next_file),False, time_format[args.time_format](*offset))
            for out_format in formats:
                c.save(out_filenames[0], languages[0], out_format)

if __name__ == "__main__":
    main()
