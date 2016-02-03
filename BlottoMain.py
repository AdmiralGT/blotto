import argparse
import itertools
import copy
import random

__author__ = 'AdmiralGT'


class BlottoPlayer(object):
    def __init__(self, string, ii):
        self.name = string[0]
        self.battlefields = []
        self.points = 0
        self.battlefield_wins = 0
        self.battlefield_draws = 0
        self.battlefield_loses = 0
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.id = ii
        for ii in range(1, 11):
            self.battlefields.append(int(string[ii]))
        self.sorted_battlefields = list(self.battlefields)
        self.sorted_battlefields.sort()
        self.battlefield_string = ','.join('%2s' % str(x) for x in self.battlefields)
        self.wins_against = []
        self.draws_against = []
        self.loses_against = []
        self.position = 100

    def __str__(self):
        self.battlefield_string = ','.join('%2s' % str(x) for x in self.battlefields)
        #return '{:3s}.{:5s} {}   {:2s}  {:2s}  {:2s}  {:3s}'.format(str(self.position),
        #                                                            self.name,
        #                                                            self.battlefield_string,
        #                                                            str(self.wins),
        #                                                            str(self.draws),
        #                                                            str(self.loses),
        #                                                            str(self.points))
        return '{:3s}.{:5s} {}   {:2s}  {:2s}  {:2s}  {:3s} {:2s} {:3s} {:3s} {:3s}'.format(str(self.position),
                                                                                            self.name,
                                                                                            self.battlefield_string,
                                                                                            str(self.wins),
                                                                                            str(self.draws),
                                                                                            str(self.loses),
                                                                                            str(self.points),
                                                                                            str(self.id),
                                                                                            str(self.battlefield_wins),
                                                                                            str(self.battlefield_draws),
                                                                                            str(self.battlefield_loses))

    def improve_player(self, iteration):
        a, b = random.sample(range(0, 10), 2)
        if iteration % 10 == 0:
            temp_battlefield = self.battlefields[a]
            self.battlefields[a] = self.battlefields[b]
            self.battlefields[b] = temp_battlefield
        else:
            if self.battlefields[b] == 0:
                if self.battlefields[a] != 0:
                    self.battlefields[b] += 1
                    self.battlefields[a] -= 1
            else:
                self.battlefields[a] += 1
                self.battlefields[b] -= 1


class BlottoMain(object):
    def __init__(self):
        self.players = []

    def main(self):
        parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
        parser.add_argument('filename', type=argparse.FileType('r'),
                            help='The file containing the blotto players')
        parser.add_argument('--debug', default=False, action='store_true', help='Print debugging information')
        args = parser.parse_args()

        self.import_players(args.filename)
        self.play_full_tournament()
        self.print_results()
        #best_players = self.find_best_player()
        #print('RESULTS')
        #for player in best_players:
        #    self.print_player_results(player)

    @staticmethod
    def print_player_results(player):
        print('Player')
        print(player)
        print('Wins:')
        for opponent in player.wins_against:
            print(opponent)
        print('Draws:')
        for opponent in player.draws_against:
            print(opponent)
        print('Loses:')
        for opponent in player.loses_against:
            print(opponent)

    def import_players(self, file):
        self.players = []
        ii = 0
        for line in file:
            line = line.rstrip()
            split_line = line.split(',')
            self.players.append(BlottoPlayer(split_line, ii))
            ii += 1

    def play_full_tournament(self):
        for game in itertools.combinations(self.players, 2):
            player_a = game[0]
            player_b = game[1]

            if player_a.sorted_battlefields == player_b.sorted_battlefields:
                player_b.id = player_a.id
            game_score = self.play_game(player_a, player_b)

            if game_score == 0:
                player_a.points += 1
                player_a.draws += 1
                player_b.points += 1
                player_b.draws += 1
            elif game_score > 0:
                player_a.points += 2
                player_a.wins += 1
                player_b.loses += 1
            else:
                player_b.points += 2
                player_b.wins += 1
                player_a.loses += 1

    @staticmethod
    def play_game(player, opponent, update_opp=True):
        game_score = 0
        for ii in range(0, 10):
            if player.battlefields[ii] > opponent.battlefields[ii]:
                game_score += 1
                player.battlefield_wins += 1
                if update_opp:
                    opponent.battlefield_loses += 1
            elif opponent.battlefields[ii] > player.battlefields[ii]:
                game_score -= 1
                player.battlefield_loses += 1
                if update_opp:
                    opponent.battlefield_wins += 1
            else:
                player.battlefield_draws += 1
                if update_opp:
                    opponent.battlefield_draws += 1
        return game_score

    def print_results(self):
        self.players.sort(key=lambda x: x.points, reverse=True)
        for player in self.players:
            player.position = self.players.index(player) + 1
            print(player)
        print()
        print()
        for player in self.players[:16]:
            self.update_score(player)
            self.print_player_results(player)
            print()
            print()

        print()
        print()
        self.players.sort(key=lambda x: x.id)
        for player in self.players:
            print(player)

    @staticmethod
    def reset_player(player):
        player.wins = 0
        player.loses = 0
        player.draws = 0
        player.points = 0
        player.wins_against = []
        player.draws_against = []
        player.loses_against = []
        player.battlefield_wins = 0
        player.battlefield_draws = 0
        player.battlefield_loses = 0

    def update_score(self, player):
        self.reset_player(player)
        for opponent in self.players:
            if player.name == opponent.name:
                continue
            game_score = self.play_game(player, opponent, False)
            if game_score == 0:
                player.draws += 1
                player.points += 1
                player.draws_against.append(opponent)
            elif game_score > 0:
                player.wins += 1
                player.points += 2
                player.wins_against.append(opponent)
            else:
                player.loses += 1
                player.loses_against.append(opponent)

    def find_best_player(self):
        best_player = BlottoPlayer(['GRT', '5', '17', '17', '1', '4', '18', '18', '8', '2', '17'], 200)
        #best_player = BlottoPlayer(['GRT', '1', '8', '19', '6', '3', '18', '4', '20', '18', '3'], 200)
        #best_player = BlottoPlayer(['GRT', '0', '12', '13', '0', '12', '12', '13', '13', '13', '12'], 200)
        test_player = copy.deepcopy(best_player)
        self.update_score(best_player)
        best_players = [best_player]

        local_iterations = 0
        total_iterations = 0
        while total_iterations < 1000000:
            test_player.improve_player(total_iterations)
            self.update_score(test_player)

            local_iterations += 1
            total_iterations += 1
            if (test_player.points > best_player.points) or ((test_player.points == best_player.points) and
                                                             local_iterations > 1000):
                if test_player.points == best_player.points:
                    present = False
                    for player in best_players:
                        if test_player.battlefields == player.battlefields:
                            present = True
                            break
                    if not present:
                        test_player.id += len(best_players)
                        best_players.append(test_player)

                    local_iterations = 0
                    test_player = copy.deepcopy(test_player)
                    self.reset_player(test_player)
                    continue
                print('New best player found on iterations {}!'.format(total_iterations))
                print(test_player)
                best_player = copy.deepcopy(test_player)
                best_players.clear()
                best_players.append(best_player)
                local_iterations = 0
            elif (test_player.points < (best_player.points - 25)) and (local_iterations > 1000):
                test_player = copy.deepcopy(best_player)
            self.reset_player(test_player)

        for player in best_players:
            self.update_score(player)
        return best_players


if __name__ == '__main__':
    blotto = BlottoMain()
    BlottoMain.main(blotto)
