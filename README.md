# pychess-assitance

* AI assist
* Chessboard to fen

![image](https://github.com/HyoungSooo/pychess-assitance/assets/86239441/715844de-ad43-4005-a773-ad98bd819eba)

### usage

* clone this repository
* download stockfish https://stockfishchess.org/download/

```python
# user_interface/interface.py
# change here
sf = Stockfish(
    path='<stockfish path>')

position = Position('captured image save path')

```

* run interface.py

* click left position and press '`' to save chessboard top left position
* click right position and pres '`' to save chessboard bottom right position

* if detected fen is not correct, click reset position and try again

* click capture to see best move and centipawn which is suggested from AI
