# Seatify
<p align='center'>
  
  <img src='https://user-images.githubusercontent.com/43326126/188296326-4c7f3244-0bdb-4306-a2ba-dc721b16f324.png' />
  
</p>

## Overview

Both [Spotify](https://developer.spotify.com/documentation/web-api/) and [SeatGeek](https://platform.seatgeek.com/?ref=publicapis.dev) offer open source API’s to access Artists and Event data respectively. What's unique with using both of these sources is that SeatGeek provides a [Spotify Artist ID in the Performers object](https://platform.seatgeek.com/?ref=publicapis.dev#performers) which therefore allows you to connect data between the two platforms. In doing this, we can draw many conclusions on popular Artists, such as understanding the total number of listens they are receiving on their songs, and how many shows they are performing this year.

The goal of this project is to create a full stack analytics project that connects both of these sources via their API’s, transform their raw data into a usable star-schema inside of a Postgres database, and present it in a meaningful way.

## Pipeline Architecture

<p align='center'>
  
  <img src=https://user-images.githubusercontent.com/43326126/191159923-9ac576c8-0fee-495a-ad49-cfb16bae44cd.png>

</p>

## ERD

[Seatify ERD (DB Diagram.io)](https://dbdiagram.io/d/62d8b5fb0d66c746551b74a5)

<p align='center'>
  
  <img src=https://user-images.githubusercontent.com/43326126/188296750-2e7e39f4-3c09-4fd9-9f73-0fce73ef2132.png>

</p>

