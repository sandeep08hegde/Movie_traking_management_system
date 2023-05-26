from tmdbv3api import TMDb,Movie,Genre
import discord
from discord.ext import commands
from discord.ui import Button,View,Select
import psycopg2 as pg
import json
from datetime import date
from discord import DMChannel

with open("./reqdata.json","rb") as js:
    jsconfig = json.load(js)
    
API_KEY = jsconfig["API_KEY"]
BOT_TOKEN = jsconfig["BOT_TOKEN"]
DB_URI = jsconfig["DB_URI"]
intents = discord.Intents.default()
intents.message_content = True


# DB RELATED STUFF

conn = pg.connect(DB_URI)
curr = conn.cursor()
conn.autocommit = True
 
def add_to_completed(ctx,movid,rating):
    movie = Movie()
    search = movie.details(movid)
    curr.execute(f"INSERT INTO completed values('{movid}','{search['title']}',{rating},'{date.today()}','{ctx.author}');")
    
def add_to_ptw(ctx,movid):
    movie = Movie()
    search = movie.details(movid)
    
    curr.execute(f"INSERT INTO plan_to_watch values('{movid}','{search['title']}','{ctx.author}');")
    
def add_to_fav(ctx,movid,rating):
    movie = Movie()
    search = movie.details(movid)
    curr.execute(f"INSERT INTO favorites values('{movid}','{search['title']}',{rating},'{ctx.author}')")


# BOT RELATED STUFF
bot = commands.Bot(command_prefix='>',intents=intents)
tmdb = TMDb()
tmdb.api_key = API_KEY
tmdb.language = 'en'
tmdb.debug = True

# sub functions events in bot command
def mov_details(movid)->list: 
    movie = Movie()  
    search = movie.details(movid)
    b = []
    g = []
    b.append(search['title'])
    b.append(search['overview'])
    for i in search['genres']:
        g.append(i['name'])
    return b,g

def movie_search(mname)->tuple:
    movie = Movie()
    search = movie.search(mname)
    st,mov_id,g = [],[],[]
    for i in search:
        st.append('' + i['title'] + " (" + i['release_date'][:4]+")")
        mov_id.append("Movie ID : " + str(i['id']))
        
    return (st, mov_id)
def ret_genres(mname):
    movie=Movie()
    search = movie.search(mname)
    g = []
    a = []
    for i in search:
        x = movie.details(i['id'])
        for j in x['genres']:
            g.append(j['name'])
        a.append(g)
    return a
            
@bot.event
async def on_ready():
    try:
        print("bot is ready!")
    except Exception as e:
        print(e)
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.reply(f"You havent passed a required argument {ctx.author.mention}. Use `>helpus` to find the function usage.")     
# BOT commands
@bot.command(name="heycine")
async def heycine(ctx):
    await ctx.reply(f"Hey! {ctx.author.mention}")

@bot.command(name="movie")
async def movie(ctx,*,mname):

    if (isinstance(ctx.channel,DMChannel)!= True and (ctx.channel.name== 'bot-testing' or ctx.channel.name == 'demo-only')) or isinstance(ctx.channel,DMChannel):
        st,mov_id= movie_search(mname)
        g = ret_genres(mname=mname)

        embed = discord.Embed(title="Search results",color=0xFF5733)
        print(len(g))
        for t in range(0,len(st)):
            embed.add_field(name=st[t],value=mov_id[t]+"\nGenre : "+", ".join(list(set(g[t]))),inline=False)
        await ctx.channel.send(embed=embed)

    else:
        await ctx.reply(f"This function can be used in DMs only {ctx.author.mention}. Please message me in DMs\nThank you!")

@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Rules to be Followed",color=0xFF5733)
    embed.add_field(name="Rule 1",value="Treat everyone with respect. Absolutely no harassment, witch hunting, sexism, racism, or hate speech will be tolerated.",inline=False)
    embed.add_field(name="Rule 2",value="No spam or self-promotion (server invites, advertisements, etc) without permission from a staff member. This includes DMing fellow members.",inline=False)
    embed.add_field(name="Rule 3",value="No age-restricted or obscene content. This includes text, images, or links featuring nudity, sex, hard violence, or other graphically disturbing content.",inline=False)
    embed.add_field(name="Rule 4",value="If you see something against the rules or something that makes you feel unsafe, let staff know. We want this server to be a welcoming space!",inline=False)
    embed.add_field(name="Rule 5",value="If there is any query you wish to ask, contact @TheDevs",inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def helpus(ctx):
    help_ops = discord.ui.Select(min_values=1,max_values=1,placeholder="Function Catalogue",
                                 options=[discord.SelectOption(label="aboutus",value=1,description="choose the option to know more"),
                                          discord.SelectOption(label="addgen",value=2,description="choose the option to know more"),
                                          discord.SelectOption(label="addmov",value=3,description="choose the option to know more"),
                                          discord.SelectOption(label="delmovie",value=4,description="choose the option to know more"),
                                          discord.SelectOption(label="genre",value=5,description="choose the option to know more"),
                                          discord.SelectOption(label="helpus",value=6,description="choose the option to know more"),
                                          discord.SelectOption(label="heycine",value=7,description="choose the option to know more"),
                                          discord.SelectOption(label="movdesc",value=8,description="choose the option to know more"),
                                          discord.SelectOption(label="movie",value=9,description="choose the option to know more"),
                                          discord.SelectOption(label="mycomp",value=10,description="choose the option to know more"),
                                          discord.SelectOption(label="myfav",value=11,description="choose the option to know more"),
                                          discord.SelectOption(label="mygen",value=12,description="choose the option to know more"),
                                          discord.SelectOption(label="myptw",value=13,description="choose the option to know more"),
                                          discord.SelectOption(label="popular",value=14,description="choose the option to know more"),
                                          discord.SelectOption(label="rules",value=15,description="choose the option to know more"),
                                          discord.SelectOption(label="topG",value=16,description="choose the option to know more"),
                                          discord.SelectOption(label="topgen",value=17,description="choose the option to know more")])
    view = View()
    view.add_item(help_ops)
    async def my_call(interaction:discord.Interaction):
        help_ops.disabled=True
        embed = discord.Embed(title="About function",color=0xFF5733)
        if help_ops.values[0] == str(1):
            embed.add_field(name=">aboutus",value="Returns a cute little description about The Devs\n"+
                            "Usage : `>aboutus`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(2):
            embed.add_field(name=">addgen",value="Allows user to add their favorite Genres\n"+
                            "Usage : `>addgen`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(3):
            embed.add_field(name=">addmov",value="Allows user to add their movies into Completed, Favorites, Plant to watch lists\n"+
                            "Usage : `>addmov <movie id>`\n> Note: The movie id must be known to the user else can be tagged along with the movies in the `>movie` function\n"
                            "Also : movies can be added into favorites if and only if the movie is in completed.")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(4):
            embed.add_field(name=">delmovie",value="Allows the user to delete a movie from their lists\n"+
                            "Usage : `>delmovie`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(5):
            embed.add_field(name=">genre",value="Allows users to view all the Genres\n"+
                            "Usage : `>genre`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(6):
            embed.add_field(name=">helpus",value="Returns a drop down list of all the functions offered by the CineTrack bot\n"+
                            "Usage : `>helpus`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(7):
            embed.add_field(name=">heycine",value="Replies to the user with 'Hey @user'\n"+
                            "Usage : `>heycine`")
            await interaction.response.edit_message(embed=embed)        
            
        elif help_ops.values[0] == str(8):
            embed.add_field(name=">movdesc",value="Gives an Overview about the movie\n"+
                            "Usage : `>movdesc <movie id>`\n> Note: The movie id must be known to the user else can be tagged along with the movies in the `>movie` function")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(9):
            embed.add_field(name=">movie",value="Allows the user to search for a movie by passing the movie name\n"+
                            "Usage : `>movie <movie name>`\n> Note: movie of any language can be searched in english alone and it handles spelling mistakes too")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(10):
            embed.add_field(name=">mycomp",value="Enables the user to view their list of completed movies\n"+
                            "Usage : `>mycomp`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(11):
            embed.add_field(name=">myfav",value="Enables the user to view their list of favorites movies\n"+
                            "Usage : `>myfav`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(12):
            embed.add_field(name=">mygen",value="Enables the user to view their list of favorite genres\n"+
                            "Usage : `>mygen`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(13):
            embed.add_field(name=">myptw",value="Enables the user to view their list of plan to watch movies\n"+
                            "Usage : `>myptw`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(14):
            embed.add_field(name=">popular",value="Returns the list of most popular movie searches in the recent history\n"+
                            "Usage : `>popular`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(15):
            embed.add_field(name=">rules",value="Lists the rules and regulations to be followed by the community\n"+
                            "Usage : `>rules`")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(16):
            embed.add_field(name=">topG",value="Retrieves the highest rated movies among the community members, the TOP5 rated movies\n"+
                            "Usage : `>topG`\nJust as they say unleash the topGs")
            await interaction.response.edit_message(embed=embed)
        elif help_ops.values[0] == str(17):
            embed.add_field(name=">topgen",value="Retrieves the ranking of the most liked genres, the TOP5 genres in the community\n"+
                            "Usage : `>topgen`")
            await interaction.response.edit_message(embed=embed)


    help_ops.callback = my_call
    await ctx.send(view=view)

@bot.command()
async def movdesc(ctx,movid):
    movie = Movie()
    search = movie.details(movid)
    embed = discord.Embed(title=search['title'],color=0xFF5733)
    embed.add_field(name="**Summary**",value=""+search['overview']+"\n**Release Date:** "+search['release_date'],inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def aboutus(ctx):
    embed = discord.Embed(title="About CineTrack",color=0xFF5733)
    embed.add_field(name="Welcome to CineTrack",value="* We as a community love and cherish movies and we hope you do so too.\n* In order to provide you that experience Aditya and Sandeep collectively have put in a lot of work into this discord bot\n* We would like to thank our movie database api provider, i.e, The Movie Database (TMDb)  without whom we are pointless\n*You can understand the functions better by calling the `>helpus` command\nBest wishes\nThe Devs")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🥰')

  
@bot.command()
async def addmov(ctx,*,movid):
    try:
        if (isinstance(ctx.channel,DMChannel)!= True and (ctx.channel.name == "bot-testing" or ctx.channel.name == 'demo-only')) or isinstance(ctx.channel,DMChannel):    
            try:
                search,gen = mov_details(movid=movid)
                selop = discord.ui.Select(min_values=1,max_values=1,placeholder="Add Movie into?",
                                    options=[discord.SelectOption(label="Completed",value="Completed",description="Add into the list of Completed movies",emoji='✅'),
                                            discord.SelectOption(label="Plan to Watch",value="ptw",description="Add movie into plan to watch list",emoji='🤔'),
                                            discord.SelectOption(label="Favorites",value="fav",description="Add movie into Favorites list",emoji='😍'),
                                            discord.SelectOption(label="Do Nothing",value="dn",description="Add nothing",emoji='❌')])

                rate_op = discord.ui.Select(min_values=1,max_values=1,placeholder="How much do u rate this movie?",
                                        options=[discord.SelectOption(label="1",value='1',description="Very Poor",emoji='🤬'),
                                                discord.SelectOption(label="2",value='2',description="Poor",emoji='☹️'),
                                                discord.SelectOption(label="3",value='3',description="Average",emoji='😐'),
                                                discord.SelectOption(label="4",value='4',description="Good",emoji='😊'),
                                                discord.SelectOption(label="5",value='5',description="Very Good",emoji='😘')])
                
                view = View()
                view.add_item(selop)
                view2 = View()
                view2.add_item(rate_op)
                embed = discord.Embed(title="Add movie into?",color=0xFF5733)
                embed.add_field(name=search[0],value=search[1]+"\nGenre : " + ", ".join(gen),inline=True)
                msg = await ctx.send(embed=embed,view=view)

                async def rate_callback(interaction : discord.Interaction):
                    if selop.values[0] == "Completed" : 
                        await interaction.response.send_message("Added to Completed list!")
                        add_to_completed(ctx,movid,int(rate_op.values[0]))      
                    elif selop.values[0] == "fav":
                        await interaction.response.send_message("Added to Favorites list!")
                        add_to_fav(ctx,movid,int(rate_op.values[0]))
                    elif selop.values[0] == "dn":
                        pass
                async def my_callback(interaction : discord.Interaction):
                    if selop.values[0] == "Completed":
                        curr.execute(f"Select * from completed where movie_id = '{movid}' and author = '{ctx.author}'")
                        if len(curr.fetchall()) != 0:
                            await ctx.send(f"You have already added this movie {ctx.author.mention}")
                        else:
                            await interaction.response.send_message("How much would you rate this movie out of 5?.",view=view2)
                            
                    
                    elif selop.values[0] == "ptw":
                        curr.execute(f"select * from plan_to_watch where movie_id = '{movid}' and author = '{ctx.author}';")
                        l = curr.fetchall()
                        if len(l)!=0:
                            await ctx.send(f"You have already added the movie into plan to watch list! {ctx.author.mention}")
                        else:
                            await interaction.response.send_message("Added to plan to watch list!")
                            add_to_ptw(ctx,movid)
                
                # considering that users must have completed the movie to add to favorites
                    else:
                        curr.execute(f"SELECT * FROM completed where movie_id = '{movid}' and author ='{ctx.author}';")
                        status_check = curr.fetchall()
                        if len(status_check) != 0:
                            await interaction.response.send_message("How much would you rate this movie out of 5?",view=view2)
                            
                        else:

                            await ctx.send("You havent watched this movie yet or have not updated the tracker")            
                
                # button on_click operations
                selop.callback = my_callback
                rate_op.callback = rate_callback
                
            except:
                await ctx.reply(f"movie id was invalid {ctx.author.mention}")
        else: 
            await ctx.reply(f"This function can be used in DMs only {ctx.author.mention}. Please message me in DMs\nThank you!")


    except:
        await ctx.reply("You havent given a movie id for me to add :(")
@bot.command()
async def popular(ctx):
    movie = Movie()
    search = movie.popular()
    embed = discord.Embed(title="Popular Movies",color=0xFF5733)
    for i in search:
       embed.add_field(name=i.title,value="Release Date : "+i.release_date,inline=False)
    
    await ctx.send(f"Here are the popular movies {ctx.author.mention}",embed=embed)
       
@bot.command()
async def mycomp(ctx):
    curr.execute(f"Select * from completed where author='{ctx.author}';")
    lt = curr.fetchall()
    if len(lt)!=0:
        embed = discord.Embed(title="Completed",color=0XFF5733)
        for i in lt:
            embed.add_field(name=i[1],value=f"Movie ID : {i[0]}\nYour rating = {i[2]}⭐",inline=False)
        
        await ctx.send(f"Here's your completed list {ctx.author.mention}",embed=embed)
    else:
        await ctx.reply(f"You haven't added movies into completed {ctx.author.mention}")
        
@bot.command()
async def myfav(ctx):
    curr.execute(f"select * from favorites where author = '{ctx.author}';")
    lt = curr.fetchall()
    if len(lt)!=0:
        embed = discord.Embed(title="Favorites",color=0xFF5733)
        for i in lt:
            embed.add_field(name=i[1],value=f"Movie ID : {i[0]}\nYour Rating = {i[2]}⭐",inline=False)
        await ctx.send(f"Here's your favorites list {ctx.author.mention}",embed=embed)
    else:
        await ctx.reply(f"You haven't added movies into favorites {ctx.author.mention}")

@bot.command()
async def myptw(ctx):
    curr.execute(f"select * from plan_to_watch where author = '{ctx.author}';")
    lt = curr.fetchall()
    if len(lt)!=0:
        embed = discord.Embed(title="Plan to Watch",color=0xFF5733)
        for i in lt:
            embed.add_field(name=i[1],value=f"Movie ID :{i[0]}",inline=False)
        await ctx.send(f"Here's your Plan to watch list {ctx.author.mention}",embed=embed)
    else:
        await ctx.reply(f"You haven't added movies into plan to watch {ctx.author.mention}")

@bot.command()
async def topG(ctx):
    curr.execute(f"Select movie_name,avg(user_rating) from completed group by movie_name order by avg(user_rating) desc;")
    lt = curr.fetchall()
    if len(lt)!=0 and len(lt) >= 6:
        embed = discord.Embed(title="Community Favorites",color=0xFF5733)
        for i in range(0,6):
            embed.add_field(name=lt[i][0],value="Average rating : {0:.2f}⭐".format(lt[i][1]),inline=False)
        
        topg = await ctx.send(f"Here are the topG's",embed=embed)
        await topg.add_reaction('👑')
    elif len(lt)<6 and len(lt) >0:
        embed = discord.Embed(title="Community Favorites",color=0xFF5733)
        for i in range(0,len(lt)):
            embed.add_field(name=lt[i][0],value="Average rating : {0:.2f}⭐".format(lt[i][1]),inline=False)
        
        topg = await ctx.send(f"Here are the topG's",embed=embed)
        await topg.add_reaction('👑')
    else:
        await ctx.reply(f"Users have not yet added movies onto completed {ctx.author.mention}") 
@bot.command()
async def genre(ctx):
    curr.execute(f"Select * from genre;")
    embed = discord.Embed(title="Genre",color=0xFF5733)
    l = curr.fetchall()
    for i in l:
        embed.add_field(name=i[1],value="Genre id : "+i[0],inline=False)
    await ctx.send(embed = embed)
    

@bot.command()
async def mygen(ctx):
    curr.execute(f"select * from my_fav_genre where author = '{ctx.author}'")
    res = curr.fetchall()
    embed = discord.Embed(title="Your Genre's",color=0xFF5733)
    if(len(res)!=0):
        for i in res:
            embed.add_field(name=i[1],value=i[0],inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.reply(f"You haven't added your genres {ctx.author.mention}")

@bot.command()
async def addgen(ctx):
    if (isinstance(ctx.channel,DMChannel)!= True and (ctx.channel.name == "bot-testing" or ctx.channel.name == 'demo-only')) or isinstance(ctx.channel,DMChannel):    
        print("hello")
        curr.execute(f"select * from my_fav_genre where author = '{ctx.author}';")
        f = curr.fetchall()
        if len(f) == 0:
            print("yes")
            curr.execute(f"select * from genre;")
            l = curr.fetchall()
            oplist = []
            for i in l:
                print(i)
                oplist.append(discord.SelectOption(label=i[1],value=(i[0]),description="genre id : "+ i[0]))
                
            selop = discord.ui.Select(min_values=2,max_values=4,placeholder="Choose Your genre",options=oplist)
            async def my_callback(interaction : discord.Interaction):
                x = []
                for i in selop.values:
                    for j in l:
                        if i in j:
                            x.append(j[1])
                        else:continue        
                for i in selop.values:            
                    curr.execute(f"insert into my_fav_genre values('{i}','{x[selop.values.index(i)]}','{ctx.author}');")
                await interaction.response.send_message(f"You added your favorite genres. Bravo {ctx.author.mention}")
            
            selop.callback = my_callback
            view = View()
            view.add_item(selop)
            await ctx.send(view=view)
        else:
            await ctx.reply(f"you have already added your favorite genres. You can edit them by calling `>editgen` {ctx.author.mention}")
    else:
        await ctx.reply(f"You can only use this in DM's {ctx.author.mention}")

@bot.command()
async def delmovie(ctx):
    if (isinstance(ctx.channel,DMChannel)!= True and (ctx.channel.name == "bot-testing" or ctx.channel.name == 'demo-only')) or isinstance(ctx.channel,DMChannel):    
        selop = discord.ui.Select(min_values=1,max_values=1,placeholder="Delete movie from?",
                                  options=[discord.SelectOption(label="Completed",value="completed",description="Delete a movie from Completed list",emoji='✅'),
                                           discord.SelectOption(label="Plan to Watch",value="ptw",description="Delete a movie from Plan to watch list",emoji='🤔'),
                                           discord.SelectOption(label="Favorites",value="fav",description="Delete a movie from favorites list",emoji='😍'),
                                           discord.SelectOption(label="Do Nothing",value="dn",description="Delete nothing",emoji='❌')])
        curr.execute(f"select * from completed where author = '{ctx.author}';")
        l1 = curr.fetchall()
        g = []
        for i in l1:
            g.append(discord.SelectOption(label=i[1],value=i[0],description="Movie id : "+i[0]))
        g.append(discord.SelectOption(label="Do Nothing",value="dn",description="Do nothing",emoji='❌'))
        curr.execute(f"select * from plan_to_watch where author = '{ctx.author}';")
        l2 = curr.fetchall()
        g1 = []
        for i in l2:
            g1.append(discord.SelectOption(label=i[1],value=i[0],description="Movie id : "+i[0]))
        g1.append(discord.SelectOption(label="Do Nothing",value="dn",description="Do nothing",emoji='❌'))
        curr.execute(f"select * from favorites where author = '{ctx.author}';")
        l3 = curr.fetchall()
        g2 = []
        for i in l3:
            g2.append(discord.SelectOption(label=i[1],value=i[0],description="Movie id : "+i[0]))
            
        g2.append(discord.SelectOption(label="Do Nothing",value="dn",description="Do nothing",emoji='❌'))
        
        del_comp = discord.ui.Select(min_values=1,max_values=1,placeholder="Choose movie to be deleted from Completed list",
                                     options=g)
        del_ptw = discord.ui.Select(min_values=1,max_values=1,placeholder="Choose a movie to be deleted from Plan to watch list",
                                    options=g1)
        del_fav = discord.ui.Select(min_values=1,max_values=1,placeholder="Choose a movie to be deleted from Favories list",
                                    options=g2)
        view = View()
        view.add_item(selop)
        view2 = View()
        
        async def my_callback(interaction : discord.Interaction):
            if selop.values[0] == "completed":
                if len(l1) != 0:
                    view2.add_item(del_comp)
                    await interaction.response.send_message("Loading your list...",view=view2)
                else:
                    await interaction.response.send_message(f"You havent added any movie to delete :) {ctx.author.mention}")
                    
            elif selop.values[0] == "fav":
                if len(l3) != 0:
                    view2.add_item(del_fav)
                    await interaction.response.send_message("Loading your list..",view=view2)
                else:
                    await interaction.response.send_message(f"You havent added any movie to delete :) {ctx.author.mention}")
            elif selop.values[0] == "ptw":
                if len(l2) != 0:
                    view2.add_item(del_ptw)
                    await interaction.response.send_message("Loading your list...",view=view2)
                else:
                    await interaction.response.send_message(f"You havent added a movie to delete :) {ctx.author.mention}")
            elif selop.values[0] == "dn":
                await interaction.response.send_message("Woohoo nothing deleted...")
            else: 
                selop.disabled=False
                await interaction.response.send_message("Ok doing nothing...")
                
        async def comp_callback(interaction : discord.Interaction):
            if del_comp.values[0] == "dn":
                await interaction.response.send_message("Ok doing nothing...")
            else:
                curr.execute(f"delete from completed where movie_id = '{del_comp.values[0]}' and author = '{ctx.author}';")
                await interaction.response.send_message(f"Movie deleted... {ctx.author.mention}")
                
        async def fav_callback(interaction : discord.Interaction):
            if del_fav.values[0] == "dn":
                await interaction.response.send_message("Ok doing nothing...")
            else:
                curr.execute(f"delete from favorites where movie_id = '{del_fav.values[0]}' and author = '{ctx.author}';")
                await interaction.response.send_message(f"Movie deleted... {ctx.author.mention}")
        async def ptw_callback(interaction:discord.Interaction):
            if del_ptw.values[0] == "dn":
                await interaction.response.send_message("Ok doing nothing...")
            else:
                curr.execute(f"delete from plan_to_watch where movie_id = '{del_ptw.values[0]}' and author = '{ctx.author}';")
                await interaction.response.send_message(f"Movie deleted... {ctx.author.mention}")
                         
        selop.callback = my_callback
        del_comp.callback = comp_callback
        del_fav.callback= fav_callback
        del_ptw.callback = ptw_callback
        await ctx.send(view=view)
    else:
        await ctx.send(f"You can only use this function in DM's {ctx.author.mention}")
        
@bot.command()
async def topgen(ctx):
    curr.execute(f"select user_genre, count(user_genre) as gen from my_fav_genre group by user_genre order by count(user_genre)desc;")
    l = curr.fetchall()
    if len(l)!=0:
        embed = discord.Embed(title="Community Favorite Genres",color=0xFF5733)
        for i in range(0,3):
            embed.add_field(name=l[i][0],value="Number of users : "+str(l[i][1]),inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👑')
    else:
        await ctx.send("😔 Users havent added favorite genres yet!")
# bot runner
bot.run(BOT_TOKEN)