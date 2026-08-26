import json
import os
import random
from pathlib import Path

STATE = Path('game/state.json')
SVG = Path('assets/tic-tac-toe.svg')

wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winner(board):
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return 'D'
    return None

def best_bot_move(board):
    # Win if possible.
    for i in range(9):
        if not board[i]:
            board[i] = 'O'
            if winner(board) == 'O':
                board[i] = ''
                return i
            board[i] = ''
    # Block X.
    for i in range(9):
        if not board[i]:
            board[i] = 'X'
            if winner(board) == 'X':
                board[i] = ''
                return i
            board[i] = ''
    for i in (4,0,2,6,8,1,3,5,7):
        if not board[i]:
            return i
    return None

def render(board, status):
    cells = []
    for i in range(9):
        row, col = divmod(i, 3)
        x, y = col * 96, row * 96
        cells.append(f'<rect x="{x}" y="{y}" width="84" height="84" rx="18" fill="#f9fafb" stroke="#d1d5db"/>')
        if board[i]:
            cells.append(f'<text x="{x+42}" y="{y+57}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="700" fill="#111827">{board[i]}</text>')

    return f'''<svg width="1100" height="420" viewBox="0 0 1100 420" xmlns="http://www.w3.org/2000/svg">
<rect width="1100" height="420" rx="28" fill="#ffffff"/>
<rect x=".5" y=".5" width="1099" height="419" rx="27.5" fill="none" stroke="#e5e7eb"/>
<text x="56" y="74" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="700" fill="#111827">Tic-Tac-Toe</text>
<text x="56" y="108" font-family="Inter,Arial,sans-serif" font-size="16" fill="#6b7280">A tiny game running on this GitHub profile</text>
<text x="56" y="168" font-family="Inter,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="1.6" fill="#9ca3af">CURRENT BOARD</text>
<g transform="translate(56,190)">{''.join(cells)}</g>
<g transform="translate(440,166)">
  <rect width="600" height="178" rx="22" fill="#f9fafb" stroke="#e5e7eb"/>
  <circle cx="36" cy="40" r="7" fill="#22c55e"/>
  <text x="56" y="46" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="700" fill="#111827">LIVE GAME</text>
  <text x="28" y="87" font-family="Inter,Arial,sans-serif" font-size="19" font-weight="600" fill="#111827">{status}</text>
  <text x="28" y="119" font-family="Inter,Arial,sans-serif" font-size="15" fill="#6b7280">You are X. The bot is O.</text>
  <text x="28" y="150" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="#374151">github-native · issue-triggered · no JavaScript</text>
</g>
</svg>'''

def main():
    state = json.loads(STATE.read_text())
    board = state['board']
    title = os.environ.get('ISSUE_TITLE', '')

    if title.startswith('tictactoe:reset'):
        board = [''] * 9
        status = 'Fresh board — your move.'
    elif title.startswith('tictactoe:'):
        try:
            move = int(title.split(':', 1)[1])
        except ValueError:
            move = -1
        if 0 <= move < 9 and not board[move] and not winner(board):
            board[move] = 'X'
            result = winner(board)
            if not result:
                bot = best_bot_move(board)
                if bot is not None:
                    board[bot] = 'O'
                result = winner(board)
            if result == 'X':
                status = 'You won. Nice.'
            elif result == 'O':
                status = 'Bot wins this round.'
            elif result == 'D':
                status = 'Draw. Clean game.'
            else:
                status = 'Your move.'
        else:
            status = 'That square is unavailable.'
    else:
        status = 'Your move.'

    state['board'] = board
    STATE.write_text(json.dumps(state, separators=(',', ':')) + '\n')
    SVG.write_text(render(board, status))

if __name__ == '__main__':
    main()
