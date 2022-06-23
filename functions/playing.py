import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from typing import List
from config import color, bad


class Playing(commands.Cog):
    @slash_command(name="가위바위보", description="봇과 가위바위보 게임을 합니다.")
    async def rsp(
        self,
        ctx: ApplicationContext,
        user: Option(str, "낼 것을 선택하세요", choices=["가위", "바위", "보"], name="선택지"),
    ):
        rsp_table = ["가위", "바위", "보"]
        if user not in rsp_table:
            embed = discord.Embed(
                title="오류 발생!", color=bad
            )
            embed.add_field(
                name="값 오류", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False
            )
            await ctx.respond(embed=embed)
        else:
            bot = random.choice(rsp_table)
            result = rsp_table.index(user) - rsp_table.index(bot)
            if result == 0:
                result = f"{user} vs {bot}\n비겼네요!"
            elif result == 1 or result == -2:
                result = f"{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!"
            else:
                result = f"{user} vs {bot}\n봇이 이겼습니다!"
            embed = discord.Embed(
                title="가위바위보",
                description=f"{ctx.author.display_name} vs 봇",
                color=color,
            )
            embed.add_field(name="**결과:**", value=f"{result}", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(name="주사위",description="주사위를 굴립니다.")
    async def dice(
        self,
        ctx: ApplicationContext,
        first: Option(int, "첫번째 숫자를 정하세요. 두번째 숫자가 없을 경우 범위는 1 ~ 수 1로 결정됩니다.", name="수1"),
        second: Option(
            int, "두번째 숫자가 있을 경우 범위는 수 1 ~ 수 2으로 결정됩니다. ", required=False, name="수2"
        ),
    ):
        try:
            if first < 1:
                embed = discord.Embed(
                    title="오류 발생!", color=0xFF0000
                )
                embed.add_field(name="값 오류", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.respond(embed=embed)
            elif second:
                embed = discord.Embed(
                    title="주사위", description=f"{first} ~ {second}", color=bad
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(first, second)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="주사위", description=f"1 ~ {first}", color=color
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(1, first)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(
                title="오류 발생!", color=bad
            )
            embed.add_field(
                name="값 오류",
                value="1. 자연수가 아닌 수를 쓰셨는지 확인해주세요.\n2. 첫번째 숫자가 두번째 숫자보다 더 큰지 확인해주세요.",
                inline=False,
            )
            await ctx.respond(embed=embed)

    @slash_command(name="홀짝", description="홀짝 게임을 시작합니다.")
    async def ode(self, ctx: ApplicationContext):
        dice = random.randint(1, 6)
        embed = discord.Embed(
            title="홀짝 게임",
            description="1부터 6까지 나오는 주사위의 수가 짝수일지, 홀수일지 아래의 반응을 눌러 예측해보세요!",
            color=color,
        )
        embed.add_field(name="> 주사위의 눈", value="?", inline=False)
        embed.add_field(name="> 선택지", value="홀수: 🔴\n짝수: 🔵", inline=True)
        interaction = await ctx.interaction.response.send_message(embed=embed)
        msg = await interaction.original_message()
        await msg.add_reaction("🔴")
        await msg.add_reaction("🔵")
        try:

            def check(reaction, user):
                return (
                    str(reaction) in ["🔴", "🔵"]
                    and user == ctx.author
                    and reaction.message.id == msg.id
                )

            reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
            if (str(reaction) == "🔴" and dice % 2 == 1) or (
                str(reaction) == "🔵" and dice % 2 == 0
            ):
                embed = discord.Embed(
                    title="홀짝 게임", description="정답입니다!", color=color
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            else:
                embed = discord.Embed(
                    title="홀짝 게임", description="틀렸습니다..", color=color
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            await msg.edit(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="오류 발생!", description="잠시 후에 다시 시도해주세요", color=bad
            )
            await msg.edit(embed=embed)

    @slash_command(name="틱택토", description="틱택토(삼목) 게임을 진행합니다.")
    async def tictactoe(
        self,
        ctx: ApplicationContext,
        rival: Option(discord.User, description="같이 게임을 할 유저를 선택하세요", name="유저"),
    ):
        if rival.bot:
            embed = discord.Embed(
                title="오류 발생!", color=bad
            )
            embed.add_field(name="오류 내용:", value="봇과는 대결할 수 없습니다.", inline=False)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(
                f"틱택토(삼목) 게임을 시작합니다. {ctx.user.mention}(X) vs {rival.mention}(O) - X부터 시작합니다.",
                view=TicTacToe(ctx.user.id, rival.id),
            )


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    styles_by_player = (discord.ButtonStyle.danger, discord.ButtonStyle.success)
    labels_by_player = ("X", "O")

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        cp = view.current_player

        assert view.board[self.y][self.x] == -1
        if interaction.user.id != view.player_ids[cp]:
            return

        view.board[self.y][self.x] = cp

        self.style = self.styles_by_player[cp]
        self.label = self.labels_by_player[cp]
        self.disabled = True

        view.current_player = cp = 1 - cp
        content = f"<@{view.player_ids[cp]}>({self.labels_by_player[cp]})의 차례입니다!"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == -1:
                content = "비겼습니다."
            else:
                content = (
                    f"<@{view.player_ids[winner]}>({self.labels_by_player[winner]}) 승리!"
                )

            for child in view.children:
                child.disabled = True
            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, player_id: discord.Member, rival_id: discord.Member):
        super().__init__()

        self.player_ids = (player_id, rival_id)

        self.current_player = 0
        self.board = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for line in range(3):
            if self.board[line][0] == self.board[line][1] == self.board[line][2] != -1:
                return self.board[line][0]

        for line in range(3):
            if self.board[0][line] == self.board[1][line] == self.board[2][line] != -1:
                return self.board[0][line]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != -1:
            return self.board[0][2]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != -1:
            return self.board[0][0]

        if all(i != -1 for row in self.board for i in row):
            return -1

        return None


def setup(bot):
    bot.add_cog(Playing())
