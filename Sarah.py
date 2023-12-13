# I imported the streamlit option menu to be able to see the side tabs for navigation. source detailed below.

# imported modules above
# I made the docstring into a comment because it kept showing up on my website...
# Class: CS230--Section 3
# Name: Sarah Beckett
# Description: This program is an interactive data-driven, web-based Python application that uses
# real-world data to display various outputs for users. This program will use Boston Trash Data, obtained
# from (http://data.boston.gov), the city of Boston’s open data hub. The data in this program specifically
# was narrowed down to 7000 random lines of that data set, due to its large size.
# I pledge that I have completed the programming assignment independently.
# Any external resources used are detailed in the code.
# I have not copied the code from a student or any source.
# I have not given my code to any student.
# Starting the functions

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
from streamlit_option_menu import option_menu


def specific_schedule(trash_dataframe, state="MA"):  # these are all MA so it is the default parameter
    input_nh = st.selectbox("Please Select Your Boston Area Neighborhood:", trash_dataframe.groupby("NEIGHBORHOOD")
                            .count().reset_index()["NEIGHBORHOOD"].tolist())
    st.write("Your Selected Neighborhood:", input_nh)  # I display what the user entered so that they can see it
    input_address = st.text_input("Please Enter your Street Address:")
    st.write("Your Street Address:", input_address)
    st.write("Your State is", state)
    input_zip = st.text_input("Please Enter your Zip Code: ")
    st.write("Your Zip Code is:", input_zip)
    row_input = trash_dataframe.loc[input_address].fillna("N/A")  # if there is no data it shows N/A not nan
    # this is cleaning the data
    # if input_address and input_zip in row_input:
    box = st.radio(f"Please confirm this is your address... {row_input.name}, {row_input['NEIGHBORHOOD']}, {state}"
                   f" {row_input['ZIP']}.", ["Yes", "No"])

    if box == "Yes":
        st.write(f"The trash gets collected at {row_input.name}, {row_input['NEIGHBORHOOD']}, {state} "
                 f"{row_input['ZIP']} on {row_input['PICKUP']} and re-collected on {row_input['RECOLLECT']}.")
        st.write("If the statement has N/A in your output, there is no available data for your address.")
        st.write(f"Below you can see all the trash data available on your address: ")
        st.caption("SAM_ID is the ID for your address in the Street Address Management System. ")
        st.caption("PWD is your Public Works District. ")
        # so the user can understand the chart better
        st.write(row_input)

    elif box == "No":
        st.write("Please re-enter your address.")


def pydeck_area(trash, color=[350, 80, 20, 200], radius=80):
    layer = pdk.Layer('ScatterplotLayer', trash, get_position=["LON", "LAT"], auto_highlight=True,
                      get_radius=radius,get_fill_color=color, pickable=True)
    view_state = pdk.ViewState(longitude=-71.0589, latitude=42.3601, zoom=10, min_zoom=1, max_zoom=15, pitch=10,
                               bearing=-27.36)
    pydeck_area_map = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(pydeck_area_map)
# https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html
# this is called 2 different times in the main function for 2 maps.


def neighborhood(data_frame):
    neighborhood = st.selectbox("Please Select Your Boston Area Neighborhood:", data_frame.groupby("NEIGHBORHOOD")
                                .count().reset_index()["NEIGHBORHOOD"].tolist())
    if neighborhood == "Boston":
        st.image("boston.jpg")
    # https://boozingabroad.com/how-to-spend-3-days-in-boston/
    elif neighborhood == "Charlestown":
        st.image("charlestown.webp")
    # https://rothgalleries.wordpress.com/2019/02/09/monument-avenue-view-of-the-bunker-hill-monument-in-charlestown-ma/
    elif neighborhood == "Roxbury":
        st.image("roxbury.jpg")
    # https://en.wikipedia.org/wiki/Lower_Roxbury_Historic_District
    elif neighborhood == "West Roxbury":
        st.image("west_roxbury.jpg")
    # https://www.bostonmagazine.com/property/neighborhood-guide-west-roxbury/
    elif neighborhood == "Brighton":
        st.image("brighton.jpg")
    # https://www.wbur.org/news/2023/09/01/brighton-boston-massachusetts-locals-field-guide
    elif neighborhood == "Mission Hill":
        st.image("mission_hill.jpg")
    # https://www.bostonmagazine.com/property/neighborhood-guide-mission-hill/
    elif neighborhood == "Dorchester":
        st.image("dorchester.jpg")
    # https://www.bostonmagazine.com/property/dorchester-neighborhood-guide/
    elif neighborhood == "Allston":
        st.image("allston.png")
    # https://www.marcroosrealty.com/allston-boston-apartments
    elif neighborhood == "East Boston":
        st.image("east_boston.jpg")
    # https://www.bostonmagazine.com/property/neighborhood-guide-east-boston/
    elif neighborhood == "Hyde Park":
        st.image("hyde_park.jpg")
    # https://www.wbur.org/news/2023/09/01/hyde-park-boston-massachusetts-locals-field-guide
    elif neighborhood == "South Boston":
        st.image("south_boston.jpg")
    # https://www.bostonmagazine.com/property/neighborhood-guide-south-boston/
    elif neighborhood == "Jamaica Plain":
        st.image("jamaica_plain.jpeg")
    # https://www.trulia.com/n/ma/boston/jamaica-plain/83569/
    elif neighborhood == "Mattapan":
        st.image("mattapan.jpg")
    # https://www.boston.gov/neighborhood/mattapan
    elif neighborhood == "Roslindale":
        st.image("roslindale.jpg")
    # https://www.bostonmagazine.com/property/roslindale-neighborhood-guide/
    elif neighborhood == "Chestnut Hill":
        st.image("chesnut_hill.jpeg")
    # https://www.alishainthe.biz/blog/visit-chestnut-hill-pa
    columns_show = ["NEIGHBORHOOD", "STATE", "ZIP", "PICKUP", "RECOLLECT", "PWD"]
    df2 = data_frame.loc[data_frame["NEIGHBORHOOD"] == neighborhood, columns_show]
    st.write(df2)


def nbhd_in_pwd(trash_data):
    selected_nbhd = st.selectbox("Please Select Your Boston Area Neighborhood:", trash_data.groupby("NEIGHBORHOOD")
                                 .count().reset_index()["NEIGHBORHOOD"].tolist(), key="unique_nbhd")
    # streamlit gave me an error saying that the select box had to have a unique key, so I added that ^
    pwd_numbers = trash_data.loc[trash_data["NEIGHBORHOOD"] == selected_nbhd, "PWD"].unique()
    # filtering the trash_data dataframe by inputted neighborhood and making sure the PWD #s are displayed
    # .unique() was a quick and efficient way to make only one of each value show up in pandas
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.unique.html
    st.write(f"The Public Works District(s) possible for your selected neighborhood, {selected_nbhd} is: "
             f"{','.join([str(pwd) for pwd in pwd_numbers])}")
    # using list comprehension to change pwd_numbers to a list


def display_pwd(trash_data):
    unique = sorted([str(pwd) for pwd in trash_data["PWD"].unique()])
    # sorting the data in the PWD column in ascending order
    user_pwd = st.selectbox("Please Select Your Boston Area Public Works District Number:", unique)
    columns_use = ["NEIGHBORHOOD", "STATE", "ZIP", "PICKUP", "RECOLLECT", "PWD"]
    # selecting only certain columns from a data frame... data analytics
    df2 = trash_data.loc[trash_data["PWD"].astype(str) == user_pwd, columns_use]
    # this data frame is created based on the filtered PWD selection and will only show the columns_use as shown.
    st.subheader(f"Trash Schedule Data Set for PWD {user_pwd}")
    st.write(df2)
    # displaying the trash data in a chart format for the user based on their inputted PWD number


def pickup_chart(trash_data):
    days = ["M", "T", "W", "TH", "F"]
    pickups_count = [trash_data["PICKUP"].value_counts().get(day, 0) for day in days]
    pickups_color = 'maroon'
    bar = 0.5
    fig, ax = plt.subplots()
    ax.bar(days, pickups_count, width=bar, label="PICKUP", color=pickups_color)
    ax.set_xlabel("Days of the Week")
    ax.set_title("Collection By Day of the Week")
    ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ax.set_ylabel("Number Collections / Day")
    ax.legend()
    st.pyplot(fig)
    # similar coding to the example we did in class


def recollect_chart(trash_data):
    days = ["M", "T", "W", "TH", "F"]
    recollect_count = [trash_data["RECOLLECT"].value_counts().get(day, 0) for day in days]
    recollect_color = 'red'
    bar = 0.5
    fig, ax = plt.subplots()
    ax.bar(days, recollect_count, width=bar, label="PICKUP", color=recollect_color)
    ax.set_xlabel("Days of the Week")
    ax.set_title("Re-Collection By Day of the Week")
    ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ax.set_ylabel("Number Re-Collections / Day")
    ax.legend()
    st.pyplot(fig)
    # similar coding to the example we did in class


def pickup_neighborhood(trash_data):
    chosen_nbhd = st.selectbox("Please Select your Neighborhood to see the Pickup Route volume for days of the week: ",
                               trash_data.groupby("NEIGHBORHOOD").count().reset_index()["NEIGHBORHOOD"].tolist(),
                               key="pick_nbhd")
    nbhd_data = trash_data[trash_data["NEIGHBORHOOD"] == chosen_nbhd]
    days = ["M", "T", "W", "TH", "F"]
    pickups_count = [nbhd_data["PICKUP"].value_counts().get(day, 0) for day in days]
    pickups_color = 'maroon'
    bar = 0.5
    fig, ax = plt.subplots()
    ax.bar(days, pickups_count, width=bar, label="PICKUP", color=pickups_color)
    ax.set_xlabel("Days of the Week")
    ax.set_title("Collection By Day of the Week")
    ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ax.set_ylabel("Number Collections / Day")
    ax.legend()
    st.pyplot(fig)

    st.write(f"Below are the number of pickups per day in {chosen_nbhd}: ")
    days_list = [f"{day}: {count}" for day, count in zip(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                                         pickups_count)]
    for day in days_list:
        st.write(day)
    busiest = max(pickups_count)
    busiest_index = pickups_count.index(busiest)
    st.write(f"The day with the most pickups in {chosen_nbhd} is {days[busiest_index]} with {busiest} pickups.")
    # this is the function that returns more than one value, the map and then this data analytics below


def recollect_neighborhood(trash_data):
    chosen_nbhd = st.selectbox("Please Select your Neighborhood to see the Re-Collection Route volume for days "
                               "of the week: ", trash_data.groupby("NEIGHBORHOOD").count().reset_index()["NEIGHBORHOOD"]
                               .tolist(), key="recollect_nbhd")
    nbhd_data = trash_data[trash_data["NEIGHBORHOOD"] == chosen_nbhd]
    days = ["M", "T", "W", "TH", "F"]
    recollect_count = [nbhd_data["RECOLLECT"].value_counts().get(day, 0) for day in days]
    recollect_color = 'red'
    bar = 0.5
    fig, ax = plt.subplots()
    ax.bar(days, recollect_count, width=bar, label="PICKUP", color=recollect_color)
    ax.set_xlabel("Days of the Week")
    ax.set_title("Re-Collection By Day of the Week")
    ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ax.set_ylabel("Number Re-Collections / Day")
    ax.legend()
    st.pyplot(fig)

    st.write(f"Below are the number of re-collections per day in {chosen_nbhd}: ")
    days_list = [f"{day}: {count}" for day, count in zip(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                                         recollect_count)]
    for day in days_list:
        st.write(day)
    busiest = max(recollect_count)
    busiest_index = recollect_count.index(busiest)
    st.write(f"The day with the most re-collections in {chosen_nbhd} is {days[busiest_index]} with "
             f"{busiest} re-collections.")


# this is the main function


def main():
    trash = pd.read_csv("BostonTrash7000.csv",
                        header=0, names=["SAM_ID", "ADDRESS", "NEIGHBORHOOD", "STATE", "ZIP", "LON", "LAT", "RECOLLECT",
                                         "PICKUP", "PWD"], index_col="ADDRESS", dtype={"ZIP": "int"})
    # reading in the data, assigning it to a data frame, and setting the address as the index for use later.
    # setting the zip code data type to input because it kept showing up as 2,119 instead of 2119.
    # how to keep the error message from displaying at the bottom
    # this is the display of the 'home' or 'welcome' page below:
    st.title("BOSTON'S TRASH COLLECTION")
    st.markdown("Please select an option from the Main Menu to the left. Scroll down to view your Menu Choice!")
    st.image("BostonView.jpg")

    # used streamlit option menu from here - https://docs.streamlit.io/library/api-reference/widgets
    # this was the best and easiest option to navigate between functionalities
    with st.sidebar:
        select = option_menu("MAIN MENU", ["Home Page", "What is Your Trash Collection Schedule?",
                                           "Map of all Boston Trash Collection Locations", "Trash Collection Schedule "
                                                                                           "Information",
                                           "Trash Collection Routes by Day", "Trash Re-Collection Routes by Day"],
                             icons=["house", "trash", "geo", "trash", "calendar", "calendar"],
                             menu_icon="signpost")

    # menu_icon is an extra pypi feature where you can display icons for different options
    # installed django-bootstrap-icons ... to get the options https://pypi.org/project/django-bootstrap-icons/
    # this is the extra credit module we have not used before

    if select == "MAIN MENU":
        pass  # I do not want anything to be done if this is selected - pass works to keep it at the welcome page

    elif select == "Home Page":
        pass  # I do not want anything to be done here either - same logic as above.
    # I still wanted to have these as options in the code, so they were accounted for

    elif select == "What is Your Trash Collection Schedule?":  # This is complete.
        st.subheader("What is Your Trash Collection Schedule?")  # Printing a sub header for the page.
        specific_schedule(trash)  # Calling the function that takes an address and gives user their trash data.

    elif select == "Map of all Boston Trash Collection Locations":
        st.subheader("Map of Trash Collection Locations in Boston: ")  # Printing a sub header for the page.
        st.markdown("Feel free to navigate around the map dragging with your cursor, and zoom as you see fit."
                    " Keep scrolling down to see a map of all trash collection locations in the neighborhood of "
                    "your choice.")
        neighborhood_list = trash["NEIGHBORHOOD"].unique()  # this unique function in pandas just prints out one
        nbhd_display = f"The different neighborhoods represented below are {', '.join(neighborhood_list)}."
        # displaying them all, so they are in a list separated by commas and a space.
        st.write(nbhd_display)
        pydeck_area(trash)
        st.subheader("Map of Trash Collection Locations in a Neighborhood:")
        input_map = st.selectbox("Please Select Your Boston Area Neighborhood to see all Collection Locations:",
                                 neighborhood_list)  # user selects neighborhood from list created above
        selected_trash = trash[trash["NEIGHBORHOOD"] == input_map]
        # filtering the data frame ^ so it only shows the data for the inputted neighborhood.
        # displaying a map for the filtered data below:
        pydeck_area(selected_trash)

    elif select == "Trash Collection Schedule Information":
        st.subheader("Trash Collection Schedule Data Set ")
        st.subheader("Trash Schedule Data Set by Neighborhood:")
        neighborhood(trash)  # displaying the data for their boston area neighborhood
        st.subheader("Trash Schedule Data Set by Public Works District: ")
        nbhd_in_pwd(trash)  # letting the user see which PWD numbers apply to their neighborhood
        display_pwd(trash)  # displaying the data for their public works district

    elif select == "Trash Collection Routes by Day":
        st.subheader("Bar Chart of Trash Collection Routes by Day of the Week")
        pickup_chart(trash)
        # I did my own analysis of the bar chart for collection routes per day of the week. below the user can see
        # what days have the most collection routes and how it affects their traffic or commute.
        st.write("The traffic in Boston's area may be most-affected by Trash Pickup Routes on Wednesday's, followed"
                 " closely by Thursday's and Tuesday's. The days of the week least-affected by Pickup Routes are "
                 "Monday's and Friday's. Keep this in mind for your morning commutes.")
        st.subheader("Bar Chart of Trash Collection Routes in Your Neighborhood by Day of the Week")
        pickup_neighborhood(trash)  # this is the same thing but for their specific neighborhoods
        # this also displays the breakdown of collections per day.

    elif select == "Trash Re-Collection Routes by Day":
        st.subheader("Bar Chart of Trash Re-Collection Routes by Day of the Week")
        recollect_chart(trash)
        st.write("The traffic in Boston's area may be most-affected by Trash Re-Collection Routes on Tuesday's. "
                 "There is a relatively high number of re-collections every day of the week.")
        st.subheader("Bar Chart of Trash Collection Routes in Your Neighborhood by Day of the Week")
        recollect_neighborhood(trash)
        # these functions have essentially the same logic, just using the re-collection data.


main()
