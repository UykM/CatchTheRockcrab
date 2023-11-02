import turtle, random, time


class RunawayGame:
    def __init__(self, canvas, runner, chaser, hp=50, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2

        # Initialize 'runner' and 'chaser'
        self.runner.shape("C:/Users/who/Downloads/rockcrab.gif")
        self.runner.penup()

        self.chaser.shape("C:/Users/who/Downloads/teemo.gif")
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        # Initialize stinger
        self.stinger = turtle.Turtle()
        self.stinger.shape("C:/Users/who/Downloads/stinger.gif")
        self.stinger.hideturtle()
        self.stinger.penup()

        self.hp = hp

        # 마지막으로 독침을 쏜 시간
        self.last_shot_time = 0

    def is_catched(self):
        p = self.runner.pos()
        q = self.stinger.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def is_collide(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def press_space(self):
        current_time = time.time()
        # 3초가 지나야 쏠 수 있다
        if current_time - self.last_shot_time >= 3:
            if self.stinger.isvisible():
                self.stinger.hideturtle()
            self.shoot_stinger()
            self.last_shot_time = current_time

    def start(self, init_dist=400, ai_timer_msec=0, stinger_speed=40):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.canvas.onkeypress(self.press_space, 'space')
        self.canvas.listen()

        self.stinger_speed = stinger_speed

        self.ai_timer_msec = ai_timer_msec
        self.start_time = time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    # 독침을 쏘는 메서드
    def shoot_stinger(self):
        if not self.stinger.isvisible():
            self.stinger.setpos(self.chaser.pos())
            self.stinger.setheading(self.chaser.heading())
            self.stinger.showturtle()

    # 스크린 밖으로 나가는 것을 방지하는 메서드
    def restrict_to_screen(self, turtle):
        screen_width = self.canvas.window_width() // 2
        screen_height = self.canvas.window_height() // 2
        x, y = turtle.pos()

        if x > screen_width:
            x = screen_width
        elif x < -screen_width:
            x = -screen_width

        if y > screen_height:
            y = screen_height
        elif y < -screen_height:
            y = -screen_height

        turtle.setpos(x, y)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.

        # 독침이 바위게에 맞았는지 체크
        if self.stinger.isvisible():
            self.stinger.forward(self.stinger_speed)
            if self.is_catched():
                self.stinger.hideturtle()
                self.hp -= 10  # 바위게의 HP 10 감소
                if self.hp <= 0:
                    self.runner.hideturtle()  # HP가 0 이하이면 사라진다
                # 독침에 맞으면 바위게가 랜덤하게 이동한다
                self.runner.goto(
                    +random.randint(300, 300), random.randint(-300, 300))

        # 바위게에 부딪혔을 때
        if self.is_collide():
            self.hp += 10  # 바위게 HP 10 회복
            self.runner.goto(
                +random.randint(300, 300), random.randint(-300, 300))

        # 시간 기록
        record_time = time.time() - self.start_time
        self.drawer.clear()
        self.drawer.setpos(200, 300)
        self.drawer.shapesize(100, 100)
        self.drawer.write(f'HP : {self.hp} / 기록 : {record_time:.0f}')

        if not self.runner.isvisible():  # 바위게를 잡았을 때
            self.drawer.goto(0, 50)
            self.drawer.write("Success", align="center", font=("", 70))
            self.drawer.goto(0, -100)
            self.drawer.write(f"{record_time:.0f}", align="center", font=("", 60))

        # 스크린 밖으로 나가지 못하게 한다
        self.restrict_to_screen(self.runner)
        self.restrict_to_screen(self.chaser)

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)


class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass


class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20, step_turn=20):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)


if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    screen = turtle.Screen()
    screen.setup(700, 700)
    screen.title("Shoot the rock crab")
    screen.bgpic("C:/Users/who/Downloads/bush.gif")
    screen.addshape("C:/Users/who/Downloads/rockcrab.gif")
    screen.addshape("C:/Users/who/Downloads/teemo.gif")
    screen.addshape("C:/Users/who/Downloads/stinger.gif")

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
