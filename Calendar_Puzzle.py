import os
import sys
import time
import numpy as np
import configparser
import matplotlib.pyplot as plt

folder = 'Pieces Set 01'
# folder = 'Pieces Set 02' # With duplicate pieces

# monthes = ['Jan']
# days = [1]
# weeks = ['Sun']
monthes = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
weeks = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat']

blank_calendar = np.zeros([8, 7])
blank_calendar[0, 6] = 1
blank_calendar[1, 6] = 1
blank_calendar[7, 0:4] = 1

# Pieces
pieces = []
config = configparser.ConfigParser()
config.read(folder + '/Pieces.ini')
num_of_pieces = len(config.sections())

for i in range(num_of_pieces):
        pieces.append([])
        pieces[i].append([])
        for j in range(len(config['Piece_' + str(i+1)])):
                temp = config['Piece_' + str(i+1)]['row_' + str(j+1)]
                temp = temp.split(' ')
                pieces[i][0].append([int(x) for x in temp])
        pieces[i][0] = np.array(pieces[i][0])
        
        # Spin the piece 4 times
        for j in range(3):
                pieces[i].append(np.transpose(pieces[i][j]))
                pieces[i][j+1] = pieces[i][j+1][::-1]

        # Flip the piece and spin it again 4 times
        pieces[i].append(pieces[i][0][::-1])
        for j in range(3):
                pieces[i].append(np.transpose(pieces[i][j+4]))
                pieces[i][j+5] = pieces[i][j+5][::-1]

        # Remove duplicants
        start = 0
        check = 1
        while start < len(pieces[i]):
                if check == len(pieces[i]):
                        start = start + 1
                        check = start + 1
                elif np.array_equal(pieces[i][start], pieces[i][check]):
                        del pieces[i][check]
                else:
                        check = check + 1

# Check if there are duplicate pieces
duplicate_pieces = []
for i in range(len(pieces)):
        duplicate_pieces.append([i+1])
skip_pieces = []
start = 0
check = 1
while start < len(pieces):
        if check == len(pieces):
                start = start + 1
                check = start + 1
                if check == len(pieces):
                        break

        if check in skip_pieces:
                check = check + 1
                continue

        for i in range(len(pieces[check])):
                if np.array_equal(pieces[start][0], pieces[check][i]):
                        duplicate_pieces[start].append(check+1)
                        skip_pieces.append(check)
                        break

        check = check + 1

for i in range(len(duplicate_pieces)-1, -1, -1):
        if len(duplicate_pieces[i]) == 1:
                del duplicate_pieces[i]

# Functions to create the solution
def month_2_calendar(month):
        global solution_text

        if   month == 'Jan':
                calendar[0, 0] = 1
                solution_text = '01-'
                x_month[0] = 1.15
                x_month[1] = 8.4
        elif month == 'Feb':
                calendar[0, 1] = 1
                solution_text = '02-'
                x_month[0] = 2.15
                x_month[1] = 8.4
        elif month == 'Mar':
                calendar[0, 2] = 1
                solution_text = '03-'
                x_month[0] = 3.15
                x_month[1] = 8.4
        elif month == 'Apr':
                calendar[0, 3] = 1
                solution_text = '04-'
                x_month[0] = 4.15
                x_month[1] = 8.4
        elif month == 'May':
                calendar[0, 4] = 1
                solution_text = '05-'
                x_month[0] = 5.15
                x_month[1] = 8.4
        elif month == 'Jun':
                calendar[0, 5] = 1
                solution_text = '06-'
                x_month[0] = 6.15
                x_month[1] = 8.4
        elif month == 'Jul':
                calendar[1, 0] = 1
                solution_text = '07-'
                x_month[0] = 1.15
                x_month[1] = 7.4
        elif month == 'Aug':
                calendar[1, 1] = 1
                solution_text = '08-'
                x_month[0] = 2.15
                x_month[1] = 7.4
        elif month == 'Sep':
                calendar[1, 2] = 1
                solution_text = '09-'
                x_month[0] = 3.15
                x_month[1] = 7.4
        elif month == 'Oct':
                calendar[1, 3] = 1
                solution_text = '10-'
                x_month[0] = 4.15
                x_month[1] = 7.4
        elif month == 'Nov':
                calendar[1, 4] = 1
                solution_text = '11-'
                x_month[0] = 5.15
                x_month[1] = 7.4
        elif month == 'Dec':
                calendar[1, 5] = 1
                solution_text = '12-'
                x_month[0] = 6.15
                x_month[1] = 7.4

def day_2_calendar(day):
        global solution_text

        div = int(day / 7)
        res = day % 7
        if res == 0:
                row = div + 1
                x_day[0] = 7
                x_day[1] = 7 - div + 0.4
        else:
                row = div + 2
                x_day[0] = res
                x_day[1] = 6 - div + 0.4

        col = res - 1
        calendar[row, col] = 1

        if day < 10:
                x_day[0] = x_day[0] + 0.375
                solution_text = solution_text + '0' + str(day) + '-'
        else:
                solution_text = solution_text + str(day) + '-'
                x_day[0] = x_day[0] + 0.25

def week_2_calendar(week):
        global solution_text

        if   week == 'Sun':
                calendar[6, 3] = 1
                solution_text = solution_text + '01'
                x_week[0] = 4.15
                x_week[1] = 2.4
        elif week == 'Mon':
                calendar[6, 4] = 1
                solution_text = solution_text + '02'
                x_week[0] = 5.15
                x_week[1] = 2.4
        elif week == 'Tues':
                calendar[6, 5] = 1
                solution_text = solution_text + '03'
                x_week[0] = 6.025
                x_week[1] = 2.4
        elif week == 'Wed':
                calendar[6, 6] = 1
                solution_text = solution_text + '04'
                x_week[0] = 7.15
                x_week[1] = 2.4
        elif week == 'Thur':
                calendar[7, 4] = 1
                solution_text = solution_text + '05'
                x_week[0] = 5.025
                x_week[1] = 1.4
        elif week == 'Fri':
                calendar[7, 5] = 1
                solution_text = solution_text + '06'
                x_week[0] = 6.15
                x_week[1] = 1.4
        elif week == 'Sat':
                calendar[7, 6] = 1
                solution_text = solution_text + '07'
                x_week[0] = 7.15
                x_week[1] = 1.4

def find_corner_zero():
        corner_zero = [8, 7]
        for i in range(len(calendar)-1, -1, -1):
                for j in range(len(calendar[0])-1, -1, -1):
                        if ((i == 0 or i == 1) and j == 6) or (i == 7 and (j == 0 or j == 1 or j == 2 or j == 3)):
                                continue

                        if calendar[i][j] == 0:
                                corner_zero[0] = i
                                corner_zero[1] = j
        
        return corner_zero

def piece_can_fit(corner_zero, piece, orient):
        col = 0
        while pieces[piece][orient][0][col] == 0:
                col = col + 1
        
        row = 0
        while pieces[piece][orient][row][0] == 0:
                row = row + 1
        if row > 0:
                row = row - 1

        if corner_zero[0] - row >= 0 and corner_zero[1] - col >= 0 and (corner_zero[0] + len(pieces[piece][orient]) - row <= 8) and (corner_zero[1] + len(pieces[piece][orient][0]) - col <= 7):
                return True
        else:
                return False

def calendar_has_two():
        for i in range(len(calendar)):
                for j in range(len(calendar[0])):
                        if calendar[i][j] == 2:
                                return True

        return False

def put_piece_in(calendar, corner_zero, piece, orient, scalar):
        col = 0
        while pieces[piece][orient][0][col] == 0:
                col = col + 1
        
        row = 0
        while pieces[piece][orient][row][0] == 0:
                row = row + 1
        if row > 0:
                row = row - 1

        calendar[corner_zero[0]-row:corner_zero[0]+len(pieces[piece][orient])-row, corner_zero[1]-col:corner_zero[1]+len(pieces[piece][orient][0])-col] += scalar * pieces[piece][orient]

def take_piece_out(corner_zero, piece, orient):
        col = 0
        while pieces[piece][orient][0][col] == 0:
                col = col + 1
        
        row = 0
        while pieces[piece][orient][row][0] == 0:
                row = row + 1
        if row > 0:
                row = row - 1

        calendar[corner_zero[0]-row:corner_zero[0]+len(pieces[piece][orient])-row, corner_zero[1]-col:corner_zero[1]+len(pieces[piece][orient][0])-col] -= pieces[piece][orient]

def is_legal(corner_zero, piece, orient):
        if piece_can_fit(corner_zero, piece, orient):
                put_piece_in(calendar, corner_zero, piece, orient, 1)

                if calendar_has_two():
                        take_piece_out(corner_zero, piece, orient)
                        return False
        else:
                return False

        return True

def create_solution(sol_pieces, sol_orient):
        global duplicate_solutions_counter
        sol = np.zeros([8, 7])
        for i in range(len(sol_pieces)):
                for j in range(len(sol_pieces[0])):
                        if sol_pieces[i][j] != 0:
                                put_piece_in(sol, [i, j], sol_pieces[i][j]-1, sol_orient[i][j]-1, sol_pieces[i][j])
        
        # If there are duplicate pieces, remove repeated solutions
        check_sol = np.zeros([8, 7])
        check_sol[:][:] = sol[:][:]
        for i in range(len(duplicate_pieces)):
                for j in range(1, len(duplicate_pieces[i]), 1):
                        check_sol[check_sol == duplicate_pieces[i][j]] = duplicate_pieces[i][0]
        
        if any(np.array_equal(check_sol, i) for i in duplicate_solutions):
                duplicate_solutions_counter = duplicate_solutions_counter + 1
                return np.zeros([8, 7])
        else:
                duplicate_solutions.append(check_sol)

        return sol

def save_solution(solution):
        global solutions_counter
        plt.figure(figsize=(10, 10))

        angles = np.linspace(0, np.pi/2, 100)
        xs = np.cos(angles) + 8
        ys = np.sin(angles) + 9
        plt.plot(xs, ys, color = 'black')
        angles = np.linspace(np.pi/2, np.pi, 100)
        xs = np.cos(angles) + 1
        ys = np.sin(angles) + 9
        plt.plot(xs, ys, color = 'black')
        angles = np.linspace(np.pi, 3*np.pi/2, 100)
        xs = np.cos(angles) + 1
        ys = np.sin(angles) + 1
        plt.plot(xs, ys, color = 'black')
        angles = np.linspace(3*np.pi/2, 2*np.pi, 100)
        xs = np.cos(angles) + 8
        ys = np.sin(angles) + 1
        plt.plot(xs, ys, color = 'black')

        xs = [1, 8]
        ys = [0, 0]
        plt.plot(xs, ys, color = 'black')
        xs = [1, 8]
        ys = [10, 10]
        plt.plot(xs, ys, color = 'black')
        xs = [0, 0]
        ys = [1, 9]
        plt.plot(xs, ys, color = 'black')
        xs = [9, 9]
        ys = [1, 9]
        plt.plot(xs, ys, color = 'black')
        xs = [1, 5, 5, 8, 8, 7, 7, 1, 1]
        ys = [2, 2, 1, 1, 7, 7, 9, 9, 2]
        plt.plot(xs, ys, color = 'black')

        plt.xlim(-0.1,  9.1)
        plt.ylim(-0.1, 10.1)
        plt.gca().set_aspect('equal')
        plt.axis('off')

        zero_count = 0
        for i in range(len(solution)):
                for j in range(len(solution[i])):
                        if ((i == 0 or i ==1) and j == 6) or (i == 7 and (j == 0 or j == 1 or j == 2 or j == 3)):
                                continue

                        if solution[i][j] == 0:
                                zero_count = zero_count + 1
                                if   zero_count == 1:
                                        plt.text(x_month[0], x_month[1], month, fontsize = 22, fontname = 'Courier New')
                                elif zero_count == 2:
                                        plt.text(x_day[0], x_day[1], day, fontsize = 22, fontname = 'Courier New')
                                elif zero_count == 3:
                                        plt.text(x_week[0], x_week[1], week, fontsize = 22, fontname = 'Courier New')

                        if j < 6:
                                if solution[i][j] != solution[i][j+1]:
                                        xs = [j + 2, j + 2]
                                        ys = [9 - i, 8 - i]
                                        plt.plot(xs, ys, color = 'black')

                        if i < 7:
                                if solution[i][j] != solution[i+1][j]:
                                        xs = [j + 1, j + 2]
                                        ys = [8 - i, 8 - i]
                                        plt.plot(xs, ys, color = 'black')

        plt.title('%s-%d-%s #%d' % (month, day, week, solutions_counter))
        plt.savefig(solution_folder + '/' + solution_text + '_' + str(solutions_counter) + '.png')
        plt.close()

# The backtracking recursive function that checks the combinations
def check_date(corner_zero, sol_pieces, sol_orient):
        global solutions_counter
        if corner_zero[0] == 8 and corner_zero[1] == 7:
                sol = create_solution(sol_pieces, sol_orient)
                if not np.array_equal(sol, np.zeros([8, 7])):
                        solutions_counter = solutions_counter + 1
                        if solutions_counter > 1:
                                sys.stdout.write("\033[F")
                        save_solution(sol)
                        print('Solution number %d saved...' % (solutions_counter))
                return

        for piece in range(len(pieces)):
                if piece + 1 in sol_pieces:
                        continue
                for orient in range(len(pieces[piece])):
                        if is_legal(corner_zero, piece, orient):
                                sol_pieces[corner_zero[0]][corner_zero[1]] = piece + 1
                                sol_orient[corner_zero[0]][corner_zero[1]] = orient + 1

                                check_date(find_corner_zero(), sol_pieces, sol_orient)

                                sol_pieces[corner_zero[0]][corner_zero[1]] = 0
                                sol_orient[corner_zero[0]][corner_zero[1]] = 0
                                take_piece_out(corner_zero, piece, orient)

# Main code
for month in monthes:
        for day in days:
                if (month == 'Feb' and (day == 30 or day == 31)) or \
                   ((month == 'Apr' or month == 'Jun' or month == 'Sep' or month == 'Nov') and day == 31):
                        continue

                for week in weeks:
                        calendar = np.zeros([8, 7])
                        calendar[:][:] = blank_calendar[:][:]

                        solution_text = ''

                        x_month = [0, 0]
                        x_day = [0, 0]
                        x_week = [0, 0]

                        month_2_calendar(month)
                        day_2_calendar(day)
                        week_2_calendar(week)

                        solution_text = solution_text + '_' + month + '-' + str(day) + '-' + week
                        solution_folder = folder + '/Solutions/' + solution_text
                        if not os.path.exists(solution_folder):
                                os.makedirs(solution_folder)

                        start_time = time.time()
                        sol_pieces = np.zeros([8, 7], dtype=int)
                        sol_orient = np.zeros([8, 7], dtype=int)
                        solutions_counter = 0
                        duplicate_solutions = []
                        duplicate_solutions_counter = 0
                        print('Searching solutions for the date: %s-%d-%s' % (month, day, week))
                        check_date(find_corner_zero(), sol_pieces, sol_orient)

                        sys.stdout.write("\033[F")
                        print('Summary for the date %s-%d-%s:' % (month, day, week))
                        print('Total solutions: %d' % (solutions_counter + duplicate_solutions_counter))
                        print('Duplicate solutions: %d' % (duplicate_solutions_counter))
                        print('Unique solutions: %d' % (solutions_counter))
                        print('Running time: %.5f seconds\n' % (time.time() - start_time))

# ======== Temp ======== #
# xs = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
# ys = [2, 9, 9, 2, 2, 9, 9, 1, 1, 9, 9, 1]
# plt.plot(xs, ys, color = 'black')
# xs = [5, 8, 8, 1, 1, 8, 8, 1, 1, 8, 8, 1, 1, 7]
# ys = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
# plt.plot(xs, ys, color = 'black')
# plt.text(1.15, 8.4, 'Jan', fontsize = 22, fontname = 'Courier New')
# plt.text(2.15, 8.4, 'Feb', fontsize = 22, fontname = 'Courier New')
# plt.text(3.15, 8.4, 'Mar', fontsize = 22, fontname = 'Courier New')
# plt.text(4.15, 8.4, 'Apr', fontsize = 22, fontname = 'Courier New')
# plt.text(5.15, 8.4, 'May', fontsize = 22, fontname = 'Courier New')
# plt.text(6.15, 8.4, 'Jun', fontsize = 22, fontname = 'Courier New')
# plt.text(1.15, 7.4, 'Jul', fontsize = 22, fontname = 'Courier New')
# plt.text(2.15, 7.4, 'Aug', fontsize = 22, fontname = 'Courier New')
# plt.text(3.15, 7.4, 'Sep', fontsize = 22, fontname = 'Courier New')
# plt.text(4.15, 7.4, 'Oct', fontsize = 22, fontname = 'Courier New')
# plt.text(5.15, 7.4, 'Nov', fontsize = 22, fontname = 'Courier New')
# plt.text(6.15, 7.4, 'Dec', fontsize = 22, fontname = 'Courier New')
# 
# plt.text(1.375, 6.4, '1', fontsize = 22, fontname = 'Courier New')
# plt.text(2.375, 6.4, '2', fontsize = 22, fontname = 'Courier New')
# plt.text(3.375, 6.4, '3', fontsize = 22, fontname = 'Courier New')
# plt.text(4.375, 6.4, '4', fontsize = 22, fontname = 'Courier New')
# plt.text(5.375, 6.4, '5', fontsize = 22, fontname = 'Courier New')
# plt.text(6.375, 6.4, '6', fontsize = 22, fontname = 'Courier New')
# plt.text(7.375, 6.4, '7', fontsize = 22, fontname = 'Courier New')
# plt.text(1.375, 5.4, '8', fontsize = 22, fontname = 'Courier New')
# plt.text(2.375, 5.4, '9', fontsize = 22, fontname = 'Courier New')
# plt.text(3.25,  5.4, '10', fontsize = 22, fontname = 'Courier New')
# plt.text(4.25,  5.4, '11', fontsize = 22, fontname = 'Courier New')
# plt.text(5.25,  5.4, '12', fontsize = 22, fontname = 'Courier New')
# plt.text(6.25,  5.4, '13', fontsize = 22, fontname = 'Courier New')
# plt.text(7.25,  5.4, '14', fontsize = 22, fontname = 'Courier New')
# plt.text(1.25,  4.4, '15', fontsize = 22, fontname = 'Courier New')
# plt.text(2.25,  4.4, '16', fontsize = 22, fontname = 'Courier New')
# plt.text(3.25,  4.4, '17', fontsize = 22, fontname = 'Courier New')
# plt.text(4.25,  4.4, '18', fontsize = 22, fontname = 'Courier New')
# plt.text(5.25,  4.4, '19', fontsize = 22, fontname = 'Courier New')
# plt.text(6.25,  4.4, '20', fontsize = 22, fontname = 'Courier New')
# plt.text(7.25,  4.4, '21', fontsize = 22, fontname = 'Courier New')
# plt.text(1.25,  3.4, '22', fontsize = 22, fontname = 'Courier New')
# plt.text(2.25,  3.4, '23', fontsize = 22, fontname = 'Courier New')
# plt.text(3.25,  3.4, '24', fontsize = 22, fontname = 'Courier New')
# plt.text(4.25,  3.4, '25', fontsize = 22, fontname = 'Courier New')
# plt.text(5.25,  3.4, '26', fontsize = 22, fontname = 'Courier New')
# plt.text(6.25,  3.4, '27', fontsize = 22, fontname = 'Courier New')
# plt.text(7.25,  3.4, '28', fontsize = 22, fontname = 'Courier New')
# plt.text(1.25,  2.4, '29', fontsize = 22, fontname = 'Courier New')
# plt.text(2.25,  2.4, '30', fontsize = 22, fontname = 'Courier New')
# plt.text(3.25,  2.4, '31', fontsize = 22, fontname = 'Courier New')
# 
# plt.text(4.15,  2.4, 'Sun', fontsize = 22, fontname = 'Courier New')
# plt.text(5.15,  2.4, 'Mon', fontsize = 22, fontname = 'Courier New')
# plt.text(6.025, 2.4, 'Tues', fontsize = 22, fontname = 'Courier New')
# plt.text(7.15,  2.4, 'Wed', fontsize = 22, fontname = 'Courier New')
# plt.text(5.025, 1.4, 'Thur', fontsize = 22, fontname = 'Courier New')
# plt.text(6.15,  1.4, 'Fri', fontsize = 22, fontname = 'Courier New')
# plt.text(7.15,  1.4, 'Sat', fontsize = 22, fontname = 'Courier New')
# ======== Temp ======== #

