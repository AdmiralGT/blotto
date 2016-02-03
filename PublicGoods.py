__author__ = 'AdmiralGT'

import matplotlib.pyplot as plt
import numpy as np
import argparse


class PublicGoods(object):

    def main(self):

        num_players = {}

        parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
        parser.add_argument('filename', type=argparse.FileType('r'),
                            help='The file containing the blotto players')
        parser.add_argument('--debug', default=False, action='store_true', help='Print debugging information')
        args = parser.parse_args()

        for ii in range(0, 35):
            num_players[ii] = 0

        for line in args.filename:
            line = line.rstrip()
            num_players[int(line)] += 1

        n_groups = 35
        index = np.arange(n_groups)
        bar_width = 0.7

        plt.bar(index, num_players.values(), bar_width, color='b', label='GRT')
        plt.xticks(np.arange(0, 35, 5))
        #plt.axvline(x=34.304, color='r')
        #plt.axvline(x=9.608695652, color='r')
        #plt.axvline(x=14.48888889, color='k')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    goods = PublicGoods()
    PublicGoods.main(goods)
