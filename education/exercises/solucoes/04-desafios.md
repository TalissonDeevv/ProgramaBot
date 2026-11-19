# Soluções: desafios práticos

## Solução do desafio D1

`bot/commands/fun/coinflip.py`:

```python
"""Comando /coinflip: cara ou coroa, com aposta opcional."""

import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed

SIDES = ("Cara", "Coroa")


def flip_coin() -> str:
    return random.choice(SIDES)


def describe_result(result: str, bet: str | None) -> str:
    """Monta o texto do resultado. Separado para facilitar os testes."""
    if bet is None:
        return f"Deu **{result}**!"
    if bet == result:
        return f"Deu **{result}**. Você acertou! 🎉"
    return f"Deu **{result}**. Não foi desta vez!"


class Coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="coinflip", description="Joga uma moeda: cara ou coroa.")
    @app_commands.describe(aposta="Seu palpite (opcional).")
    @app_commands.choices(aposta=[app_commands.Choice(name=side, value=side) for side in SIDES])
    async def coinflip(
        self,
        interaction: discord.Interaction,
        aposta: app_commands.Choice[str] | None = None,
    ) -> None:
        result = flip_coin()
        text = describe_result(result, aposta.value if aposta else None)
        await interaction.response.send_message(embed=base_embed("🪙 Cara ou coroa", text))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Coinflip(bot))
```

Testes:

```python
from bot.commands.fun.coinflip import SIDES, describe_result, flip_coin

def test_flip_coin():
    assert all(flip_coin() in SIDES for _ in range(50))

def test_describe_result():
    assert "acertou" in describe_result("Cara", "Cara")
    assert "Não foi" in describe_result("Cara", "Coroa")
    assert describe_result("Coroa", None) == "Deu **Coroa**!"
```

Mais: entrada no `/help`, `"coinflip"` em `EXPECTED_SLASH_COMMANDS`, `education/code-explanation/commands/fun/coinflip.md` e, no CHANGELOG, em "Não lançado > Adicionado": "Comando `/coinflip`".

## Solução do desafio D2

Estrutura sugerida:

```
bot/data/quiz.json
bot/views/quiz.py            ← lógica + view
bot/commands/fun/quiz.py     ← comando
```

`bot/data/quiz.json`:

```json
{
  "questions": [
    {
      "question": "Qual palavra-chave define uma função em Python?",
      "options": ["func", "def", "function", "lambda"],
      "answer": 1
    },
    {
      "question": "Qual tipo representa verdadeiro/falso?",
      "options": ["int", "str", "bool", "list"],
      "answer": 2
    }
  ]
}
```

`bot/views/quiz.py`:

```python
import json
from dataclasses import dataclass
from pathlib import Path

import discord

QUIZ_FILE = Path(__file__).resolve().parent.parent / "data" / "quiz.json"


@dataclass(frozen=True)
class Question:
    text: str
    options: list[str]
    answer: int

    def is_correct(self, index: int) -> bool:
        return index == self.answer


def load_questions(path: Path = QUIZ_FILE) -> list[Question]:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    questions = []
    for item in data["questions"]:
        if len(item["options"]) != 4 or not 0 <= item["answer"] < 4:
            raise ValueError(f"Pergunta inválida: {item['question']!r}")
        questions.append(Question(item["question"], item["options"], item["answer"]))
    return questions


class AnswerButton(discord.ui.Button["QuizView"]):
    def __init__(self, index: int, label: str) -> None:
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index = index

    async def callback(self, interaction: discord.Interaction) -> None:
        view = self.view
        if view is None:
            return
        correct = view.question.is_correct(self.index)
        for button in view.children:
            button.disabled = True
            if button.index == view.question.answer:
                button.style = discord.ButtonStyle.success
        if not correct:
            self.style = discord.ButtonStyle.danger
        view.stop()
        text = "✅ Resposta certa!" if correct else "❌ Resposta errada."
        await interaction.response.edit_message(content=text, view=view)


class QuizView(discord.ui.View):
    def __init__(self, question: Question, author_id: int) -> None:
        super().__init__(timeout=60)
        self.question = question
        self.author_id = author_id
        for index, option in enumerate(question.options):
            self.add_item(AnswerButton(index, option))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Este quiz é de outra pessoa.", ephemeral=True)
            return False
        return True
```

`bot/commands/fun/quiz.py`:

```python
import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.views.quiz import QuizView, load_questions


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.questions = load_questions()

    @app_commands.command(name="quiz", description="Responda uma pergunta de programação.")
    async def quiz(self, interaction: discord.Interaction) -> None:
        question = random.choice(self.questions)
        await interaction.response.send_message(
            f"❓ **{question.text}**", view=QuizView(question, interaction.user.id)
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Quiz(bot))
```

**Comentários:** `load_questions` e `Question.is_correct` são testáveis sem o Discord. Há dois arquivos Python novos, então são duas páginas de documentação novas (`views/quiz.md` e `commands/fun/quiz.md`).

## Solução do desafio D3

Em `bot/database/reminders.py`, faça `_execute` devolver também o `rowcount` e adicione dois métodos:

```python
    def _execute(self, query: str, parameters: tuple = ()) -> tuple[list[sqlite3.Row], int | None, int]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                cursor = connection.execute(query, parameters)
                return cursor.fetchall(), cursor.lastrowid, cursor.rowcount
        finally:
            connection.close()

    def list_for_user(self, user_id: int) -> list[Reminder]:
        rows, _, _ = self._execute(
            "SELECT id, user_id, channel_id, message, remind_at FROM reminders "
            "WHERE user_id = ? ORDER BY remind_at",
            (user_id,),
        )
        return [self._row_to_reminder(row) for row in rows]

    def delete_for_user(self, reminder_id: int, user_id: int) -> bool:
        """Apaga só se o lembrete for da pessoa. Retorna True se apagou."""
        _, _, deleted = self._execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?", (reminder_id, user_id)
        )
        return deleted > 0
```

Lembre-se de atualizar as outras chamadas de `_execute` para desempacotar três valores (`rows, _, _ = ...`).

No Cog do `/remind`:

```python
    @app_commands.command(name="reminders", description="Lista os seus lembretes pendentes.")
    @app_commands.guild_only()
    async def reminders(self, interaction: discord.Interaction) -> None:
        items = self.repository.list_for_user(interaction.user.id)
        if not items:
            await interaction.response.send_message(embed=info_embed("Você não tem lembretes."), ephemeral=True)
            return
        lines = [f"**#{r.id}** {discord.utils.format_dt(r.remind_at, 'R')}: {r.message}" for r in items]
        await interaction.response.send_message(embed=info_embed("\n".join(lines), title="⏰ Seus lembretes"), ephemeral=True)

    @app_commands.command(name="remind-cancel", description="Cancela um lembrete seu.")
    @app_commands.describe(id="Número do lembrete (veja em /reminders).")
    @app_commands.guild_only()
    async def remind_cancel(self, interaction: discord.Interaction, id: int) -> None:
        if self.repository.delete_for_user(id, interaction.user.id):
            await interaction.response.send_message(embed=success_embed(f"Lembrete #{id} cancelado."), ephemeral=True)
        else:
            await interaction.response.send_message(embed=error_embed("Lembrete não encontrado."), ephemeral=True)
```

Teste de segurança:

```python
def test_cannot_delete_other_users_reminder(repository):
    reminder_id = repository.add(1, 10, "meu", datetime.now(timezone.utc))
    assert repository.delete_for_user(reminder_id, user_id=2) is False
    assert repository.count_for_user(1) == 1
```

**Comentários:** o `AND user_id = ?` no SQL é o que garante a segurança. Verificar no Python depois de buscar também funcionaria, mas fazer no banco é mais simples e não tem brechas. O parâmetro se chama `id` para aparecer assim no Discord; dentro da função, ele esconde a função nativa `id()`, o que não causa problema aqui.

## Solução do desafio D4

Em `bot/views/confirm.py`:

```python
from bot.utils.embeds import info_embed, warning_embed


async def confirm_action(interaction: discord.Interaction, description: str) -> bool:
    """Pede confirmação. Retorna True só se a pessoa confirmou.

    Em caso de cancelamento ou tempo esgotado, já edita a mensagem explicando.
    """
    view = ConfirmView(author_id=interaction.user.id)
    await interaction.response.send_message(embed=warning_embed(description), view=view, ephemeral=True)
    await view.wait()

    if view.confirmed is None:
        await interaction.edit_original_response(embed=info_embed("Tempo esgotado. Nada foi feito."), view=None)
        return False
    if not view.confirmed:
        await interaction.edit_original_response(embed=info_embed("Ação cancelada."), view=None)
        return False
    return True
```

No `/kick` (o `/ban` fica igual):

```python
        if not await confirm_action(interaction, f"Tem certeza que deseja **expulsar** {membro.mention}?"):
            return

        try:
            await membro.kick(reason=build_audit_reason(motivo, interaction.user, "kick"))
        ...
```

**Comentários:** cerca de 15 linhas repetidas viram uma chamada. Como o retorno virou `bool`, quem chama não precisa conhecer os três estados de `ConfirmView`. Atualize as documentações de `confirm.md`, `kick.md` e `ban.md`.
