import flet as ft
import asyncio
import aiohttp

actualPokemon = 0 # Global variable to make petitions

async def main(page: ft.Page):
    # Initialize the principal screen
    page.window_width = 500
    page.window_height = 650
    page.window_resizable = False
    page.padding = 0
    page.margin = 0
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")

    # Program functions

    async def petition(url): # Get pokemon
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
            
    async def getPokemon(e: ft.ContainerTapEvent):
        global actualPokemon
        if e.control == upArrow:
            actualPokemon += 1
        else:
            actualPokemon -=1
        id = (actualPokemon%150)+1 # It reset the count once it reaches 150 
        result = await petition(f"https://pokeapi.co/api/v2/pokemon/{id}")
        
        data =f"Number:{id}\nName: {result['name']}\n\nAbilities:"
        for element in result['abilities']:
            ability = element['ability']['name']
            data += f"\n{ability}"
        data += f"\nHeight: {result['height']}"
        text.value = data
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        image.src = sprite_url
        await page.update_async()
    
    async def blink():
        while True:
            await asyncio.sleep(1)
            blueLight.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            blueLight.bgcolor = ft.colors.BLUE
            await page.update_async()

    # Program interface
    blueLight = ft.Container(width=30, height=30, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=50)
    blueButton = ft.Stack([
        ft.Container(width=40, height=40, bgcolor=ft.colors.WHITE, border_radius=50),
        blueLight,
        ]
    )

    topItems = [
        ft.Container(blueButton, width=40, height=40),
        ft.Container(width=20, height=20, bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=20, height=20, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=20, height=20, bgcolor=ft.colors.GREEN, border_radius=50),
    ]

    image = ft.Image(
        src = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png",
        scale=5,
        width=30,
        height=30,
        top=150/2,
        right=350/2,
    )

    centralStack = ft.Stack(
        [
            ft.Container(width=400, height=200, bgcolor=ft.colors.WHITE, border_radius=20),
            ft.Container(width=350, height=150, bgcolor=ft.colors.BLACK, top=25, left=25),
            image,
        ]
    )

    triangle = ft.canvas.Canvas([
    ft.canvas.Path(
        [
            ft.canvas.Path.MoveTo(20, 0),
            ft.canvas.Path.LineTo(0, 25),
            ft.canvas.Path.LineTo(40, 25),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL
            ),
            ),
        ],
        width=80,
        height=50,
    )
    upArrow = ft.Container(triangle, width=40, height=25, on_click=getPokemon)
    
    arrows = ft.Column(
        [
            upArrow,
            ft.Container(triangle, width=40, height=25, rotate=ft.Rotate(angle=3.14159), on_click=getPokemon)
        ]
    )

    text = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=12,
    )

    inferiorItems = [
        ft.Container(width=80),
        ft.Container(text, padding=20, width=200, height=170, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=30),
        ft.Container(arrows, width=80, height=50),
    ]

    top = ft.Container(content=ft.Row(topItems), width=500, height=40, margin=ft.margin.only(top=40))
    center = ft.Container(centralStack, width=500,height=200, margin = ft.margin.only(top=40), alignment=ft.alignment.center)
    bottom = ft.Container(content=ft.Row(inferiorItems), width=500,height=300)
    
    col = ft.Column(spacing=0, controls=[
        top,
        center,
        bottom
    ])

    container = ft.Container(col, width=500, height=600, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(container)
    await blink()

ft.app(target=main)