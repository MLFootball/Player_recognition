from scrapper import HLTVPlayer
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'cli.py',
                    description = 'Program takes link to  player, scrapes stats by caching html pages in \
                            folder data/player and produces json file with scraped stats')
    parser.add_argument('url', type=str, help="Url to profile of the player")           # positional argument
    parser.add_argument('-p', '--project_dir', type=str, default=".", help="Path where cached results and scrapped stats should be stored. By default: current working directory.")      # option that takes a value
    parser.add_argument('-o', '--outname', type=str, default="", help="Name of the json with scraped results saved in directory results. By default: playerName_stats_date.json")      # option that takes a value
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag

    args = parser.parse_args()
    player = HLTVPlayer(url = args.url, project_dir=args.project_dir, verbose=args.verbose, outname=args.outname)
    player.cache_all_pages()
    player.save_stats(player.get_stats())
