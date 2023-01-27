from ajax_table import TorMediaItem, TorcpItemDBObj, queryByHash
import os, sys
from torcp.torcp import Torcp
from myconfig import CONFIG
import argparse


def runTorcp(torpath, torhash, torsize):
    if torpath and torhash and torsize:
        npath = os.path.normpath(torpath.strip())
        torname = os.path.basename(npath)
        site_id_imdb = os.path.basename(os.path.dirname(npath))
        site = ''
        siteid = ''
        torimdb = ''
        if "_" in site_id_imdb:
            l = site_id_imdb.split("_")
            if len(l) == 3:
                site, siteid, torimdb = l[0], l[1], l[2]
            elif len(l) == 2:
                site, siteid = l[0], l[1]

        targetDir = os.path.join(CONFIG.linkDir, torhash)
        argv = [npath, "-d", targetDir, "-s", 
                "--lang", CONFIG.lang, 
                "--tmdb-api-key", CONFIG.tmdb_api_key, 
                "--tmdb-lang", CONFIG.tmdbLang, 
                "--imdbid", torimdb, 
                "--make-log", CONFIG.bracket, 
                "-e", "srt",
                "--extract-bdmv", "--tmdb-origin-name"]
        eo = TorcpItemDBObj(site, siteid, torimdb, torhash.strip(), int(torsize.strip()))
        o = Torcp()
        o.main(argv, eo)
        return  200
    return  401


def loadArgs():
    parser = argparse.ArgumentParser(description='wrapper to TORCP to save log in sqlite db.')
    parser.add_argument('-F', '--full-path', help='full torrent save path.')
    parser.add_argument('-I', '--info-hash', help='info hash of the torrent.')
    parser.add_argument('-G', '--tag', help='tag of the torrent.')
    parser.add_argument('-Z', '--size', help='size of the torrent.')

    global ARGS
    ARGS = parser.parse_args()


def main():
    loadArgs()
    runTorcp(ARGS.full_path, ARGS.info_hash, ARGS.size)


if __name__ == '__main__':
    main()