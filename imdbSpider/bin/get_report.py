# coding=UTF-8
import lib_noti
import argparse
import datetime as dt


# provide the report depending on the reports keyword
def main(stats_date, reports):
    if reports == "favourite-new":
        msg = "imdb: start favourite and new spiders\n" + \
              "favourite.csv: " + "http://static.abcedf.com/turbo/imdb/favourite.csv\n" + \
              "new.csv: " + "http://static.abcedf.com/turbo/imdb/new.csv\n"
        lib_noti.send(msg)
        print("Favourite And New csv Files Arrived successfully!")
        return
    elif reports == 'list':
        msg = "imdb: start list spider\n" + \
              "favourite.csv: " + "http://static.abcedf.com/turbo/imdb/list.csv\n"
        lib_noti.send(msg)
        print("List csv Files Arrived successfully!")
        return
    else:
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-s', '--stats_date', dest='stats_date',
        default=dt.datetime.strftime(dt.datetime.now() - dt.timedelta(1), '%Y-%m-%d'),
        help='The Date That To Be Loaded, Default Value Is Yesterday')
    parser.add_argument(
        '-r', '--reports', dest='reports',
        default="favourite-new",
        help='Which reports should be sent to DingTalk')
    args = parser.parse_args()
    main(**vars(args))