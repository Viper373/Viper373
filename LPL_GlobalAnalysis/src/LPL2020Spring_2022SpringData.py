###################################################################################################################################################################################################
##########################################################################################  载入第三方模块  ##########################################################################################
import requests  # 访问数据API接口
import json  # 数据解析模块
from selenium import webdriver  # 拟人爬取数据模块
from bs4 import BeautifulSoup  # 基于selenium模块获取到的数据解析工具
from tqdm import tqdm  # 进度条模块
from selenium.webdriver.common.by import By  # 控制浏览器模拟鼠标动作模块
from selenium.webdriver.edge.service import Service  # selenium模块启动edge浏览器服务
from sqlalchemy import create_engine  # 依赖pandas的dataframe的写入数据库模块
import pymysql  # mysql数据库模块
import time  # 时间模块
import pandas as pd  # 数据处理
import re  # 正则表达式


startTime = time.perf_counter()  # 记录完整开始时间
print("LPL2020Spring~2022Spring数据采集开始——————————")
####################################################################################################################################################################################################
####################################################################################  建立与本地MySQL数据库的连接  ####################################################################################
sylpol = pymysql.connect(host='localhost', user='root', password='ShadowZed666', db='LeagueofLegendsProLeague',
                         port=3306, charset='utf8mb4')
mycursor = sylpol.cursor()  # 获取游标

####################################################################################################################################################################################################
#########################################################################  创建存储数据的数据表（15张表：2020春季赛-2022春季赛） #########################################################################
start = time.perf_counter()  # 记录创建数据表开始时间

## LPL2020春季赛战队表
mycursor.execute('DROP TABLE IF EXISTS lpl2020SpringTeam')  # 如果该表存在，则删除
sql_teamTable = "CREATE TABLE `lpl2020springteam`  (`trank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                "`team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '战队名'," \
                "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                "`win_lose` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜/负'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                "`baron_perGame` decimal(2, 1) NULL DEFAULT 0.0 COMMENT '场均大龙'," \
                "`dragon_perGame` decimal(2, 1) NULL DEFAULT 0.0 COMMENT '场均小龙')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_teamTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020春季赛team表成功，准备创建LPL2020春季赛player表……")
except Exception as e:
    print("创建LPL2020春季赛team表失败：case%s" % e)

## LPL2020春季赛个人表
mycursor.execute('DROP TABLE IF EXISTS lpl2020springplayer')  # 如果该表存在，则删除
sql_playerTable = "CREATE TABLE `lpl2020springplayer`  (`prank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                  "`player` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '队员'," \
                  "`position` varchar(20) NULL DEFAULT NULL COMMENT '位置'," \
                  "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                  "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                  "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                  "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                  "`killDieAssist` decimal(10,2) NULL DEFAULT NULL COMMENT 'KDA'," \
                  "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                  "`creepScore_perGame` int(10) NULL DEFAULT 0 COMMENT '场均补刀'," \
                  "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                  "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                  "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                  "`modelViewPresenter` int(10) NULL DEFAULT 0 COMMENT 'MVP次数')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_playerTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020春季赛player表成功，准备创建LPL2020春季赛hero表……")
except Exception as e:
    print("创建LPL2020春季赛player表失败：case%s" % e)

## LPL2020春季赛hero表
mycursor.execute('DROP TABLE IF EXISTS lpl2020springhero')  # 如果该表存在，则删除
sql_heroTable = "CREATE TABLE `lpl2020springhero`  (`hrank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                "`hero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '英雄名'," \
                "`appearance` int(10) NULL DEFAULT NULL COMMENT '出场次数'," \
                "`pickRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pick比率'," \
                "`banRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ban比率'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                "`commonPlayers` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常用队员')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_heroTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020春季赛hero表成功，准备创建LPL2020夏季赛team表")
except Exception as e:
    print("创建LPL2020春季赛hero表失败：case%s" % e)

## LPL2020夏季赛team表
mycursor.execute('DROP TABLE IF EXISTS lpl2020summerteam')  # 如果该表存在，则删除
sql_teamTable = "CREATE TABLE `lpl2020summerteam`  (`trank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                "`team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '战队名'," \
                "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                "`win_lose` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜/负'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                "`baron_perGame` decimal(2, 1) NULL DEFAULT 0.0 COMMENT '场均大龙'," \
                "`dragon_perGame` decimal(2, 1) NULL DEFAULT 0.0 COMMENT '场均小龙')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_teamTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020夏季赛team表成功，准备创建LPL2020夏季赛player表……")
except Exception as e:
    print("创建LPL2020夏季赛team表失败：case%s" % e)

## LPL2020夏季赛player表
mycursor.execute('DROP TABLE IF EXISTS lpl2020summerplayer')  # 如果该表存在，则删除
sql_playerTable = "CREATE TABLE `lpl2020summerplayer`  (`prank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                  "`player` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '队员'," \
                  "`position` varchar(20) NULL DEFAULT NULL COMMENT '位置'," \
                  "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                  "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                  "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                  "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                  "`killDieAssist` decimal(10,2) NULL DEFAULT NULL COMMENT 'KDA'," \
                  "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                  "`creepScore_perGame` int(10) NULL DEFAULT 0 COMMENT '场均补刀'," \
                  "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                  "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                  "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                  "`modelViewPresenter` int(10) NULL DEFAULT 0 COMMENT 'MVP次数')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_playerTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020夏季赛player表成功，准备创建LPL2020夏季赛hero表……")
except Exception as e:
    print("创建LPL2020夏季赛player表失败：case%s" % e)

## LPL2020夏季赛hero表
mycursor.execute('DROP TABLE IF EXISTS lpl2020summerhero')  # 如果该表存在，则删除
sql_heroTable = "CREATE TABLE `lpl2020summerhero`  (`hrank` int(10) UNIQUE PRIMARY KEY COMMENT '排名'," \
                "`hero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '英雄名'," \
                "`appearance` int(10) NULL DEFAULT NULL COMMENT '出场次数'," \
                "`pickRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pick比率'," \
                "`banRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ban比率'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                "`commonPlayers` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常用队员')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_heroTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2020夏季赛hero表成功，准备创建LPL2021春季赛team表")
except Exception as e:
    print("创建LPL2020夏季赛hero表失败：case%s" % e)

## LPL2021春季赛team表
mycursor.execute('DROP TABLE IF EXISTS lpl2021springteam')  # 如果该表存在，则删除
sql_teamTable = "CREATE TABLE `lpl2021springteam`  (`trank` int(10) NULL COMMENT '排名'," \
                "`team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '战队名'," \
                "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                "`win_lose` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜/负'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                "`baron_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均大龙'," \
                "`dragon_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均小龙')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_teamTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2021春季team表成功，准备创建LPL2021年春季赛player表……")
except Exception as e:
    print("创建LPL2021年春季赛team表失败：case%s" % e)

## LPL2021春季赛player表
mycursor.execute('DROP TABLE IF EXISTS lpl2021springplayer')  # 如果该表存在，则删除
sql_playerTable = "CREATE TABLE `lpl2021springplayer`  (`prank` int(10) NOT NULL COMMENT '排名'," \
                  "`player` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '选手名'," \
                  "`position` varchar(20) NULL DEFAULT NULL COMMENT '位置'," \
                  "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                  "`modelViewPresenter` int(10) NULL DEFAULT 0 COMMENT 'MVP次数'," \
                  "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                  "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                  "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                  "`killDieAssist` int(10) NULL DEFAULT NULL COMMENT 'KDA'," \
                  "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                  "`creepScore_perGame` int(10) NULL DEFAULT 0 COMMENT '场均补刀'," \
                  "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                  "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                  "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                  "`contrapositionEconomicDifference` int(10) NULL DEFAULT NULL COMMENT '场均对位经济差'," \
                  "`damage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '伤害占比'," \
                  "`gold` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '经济占比')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_playerTable)  # 执行sql语句
    print("创建LPL2021年春季赛player表成功，准备创建LPL2021年春季赛hero表……")
except Exception as e:
    print("创建LPL2021年春季赛player表失败：case%s" % e)

## LPL2021春季赛hero表
mycursor.execute('DROP TABLE IF EXISTS lpl2021SpringHero')  # 如果该表存在，则删除
sql_heroTable = "CREATE TABLE `lpl2021SpringHero`  (`hrank` int(10) NULL COMMENT '排名'," \
                "`hero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '英雄名'," \
                "`appearance` int(10) NULL DEFAULT NULL COMMENT '出场次数'," \
                "`pickRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pick比率'," \
                "`banRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ban率'," \
                "`winRate` varchar(20) CHARACTER  SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`killDieAssist` double(10, 2) NULL DEFAULT 0.00 COMMENT 'KDA'," \
                "`commonPlayers` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常用队员')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_heroTable)  # 执行sql语句
    print("创建LPL2021年春季赛hero表成功，准备创建LPL2021夏季赛team表……")
except Exception as e:
    print("创建LPL2021年春季赛hero表失败：case%s" % e)

## LPL2021夏季赛team表
mycursor.execute('DROP TABLE IF EXISTS lpl2021summerteam')  # 如果该表存在，则删除
sql_teamTable = "CREATE TABLE `lpl2021summerteam`  (`trank` int(10) NULL COMMENT '排名'," \
                "`team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '战队名'," \
                "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                "`win_lose` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜/负'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                "`baron_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均大龙'," \
                "`dragon_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均小龙')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_teamTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2021夏季赛team表成功，准备创建LPL2021夏季赛player表……")
except Exception as e:
    print("创建LPL2021夏季赛team表失败：case%s" % e)

## LPL2021夏季赛player表
mycursor.execute('DROP TABLE IF EXISTS lpl2021summerplayer')  # 如果该表存在，则删除
sql_playerTable = "CREATE TABLE `lpl2021summerplayer`  (`prank` int(10) NOT NULL COMMENT '排名'," \
                  "`player` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '选手名'," \
                  "`position` varchar(20) NULL DEFAULT NULL COMMENT '位置'," \
                  "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                  "`modelViewPresenter` int(10) NULL DEFAULT 0 COMMENT 'MVP次数'," \
                  "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                  "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                  "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                  "`killDieAssist` decimal(10,2) NULL DEFAULT NULL COMMENT 'KDA'," \
                  "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                  "`creepScore_perGame` int(10) NULL DEFAULT 0 COMMENT '场均补刀'," \
                  "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                  "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                  "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                  "`contrapositionEconomicDifference` int(10) NULL DEFAULT NULL COMMENT '场均对位经济差'," \
                  "`damage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '伤害占比'," \
                  "`gold` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '经济占比')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_playerTable)  # 执行sql语句
    print("创建LPL2021夏季赛player表成功，准备创建LPL2021夏季赛hero表……")
except Exception as e:
    print("创建LPL2021夏季赛player表失败：case%s" % e)

## LPL2021夏季赛hero表
mycursor.execute('DROP TABLE IF EXISTS lpl2021summerhero')  # 如果该表存在，则删除
sql_heroTable = "CREATE TABLE `lpl2021summerhero`  (`hrank` int(10) NULL COMMENT '排名'," \
                "`hero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '英雄名'," \
                "`appearance` int(10) NULL DEFAULT NULL COMMENT '出场次数'," \
                "`pickRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pick比率'," \
                "`banRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ban率'," \
                "`winRate` varchar(20) CHARACTER  SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`killDieAssist` double(10, 2) NULL DEFAULT 0.00 COMMENT 'KDA'," \
                "`commonPlayers` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常用队员')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_heroTable)  # 执行sql语句
    print("创建LPL2021夏季赛hero表成功，准备创建LPL2022春季赛team表……")
except Exception as e:
    print("创建LPL2021夏季赛hero表失败：case%s" % e)

## LPL2022春季赛team表
mycursor.execute('DROP TABLE IF EXISTS lpl2022springteam')  # 如果该表存在，则删除
sql_teamTable = "CREATE TABLE `lpl2022SpringTeam`  (`trank` int(10) NULL COMMENT '排名'," \
                "`team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '战队名'," \
                "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                "`win_lose` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜/负'," \
                "`winRate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                "`baron_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均大龙'," \
                "`dragon_perGame` float(10, 1) NULL DEFAULT 0.0 COMMENT '场均小龙')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_teamTable)  # 执行sql语句
    sylpol.commit()
    print("创建LPL2022春季赛team表成功，准备创建LPL2022春季赛player表……")
except Exception as e:
    print("创建LPL2021春季赛team表失败：case%s" % e)

## LPL2022春季赛player表
mycursor.execute('DROP TABLE IF EXISTS lpl2022springplayer')
sql_playerTable = "CREATE TABLE `lpl2022springplayer`  (`prank` int(10) NOT NULL COMMENT '排名'," \
                  "`player` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '选手名'," \
                  "`position` varchar(20) NULL DEFAULT NULL COMMENT '位置'," \
                  "`appearance` int(10) NULL DEFAULT 0 COMMENT '出场次数'," \
                  "`modelViewPresenter` int(10) NULL DEFAULT 0 COMMENT 'MVP次数'," \
                  "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                  "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                  "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                  "`killDieAssist` int(10) NULL DEFAULT NULL COMMENT 'KDA'," \
                  "`money_perGame` int(10) UNSIGNED NULL DEFAULT 0 COMMENT '场均金钱'," \
                  "`creepScore_perGame` int(10) NULL DEFAULT 0 COMMENT '场均补刀'," \
                  "`catchEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均插眼'," \
                  "`rowEye_perGame` int(10) NULL DEFAULT 0 COMMENT '场均排眼'," \
                  "`attendanceRate_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '场均参团率'," \
                  "`contrapositionEconomicDifference` int(10) NULL DEFAULT NULL COMMENT '场均对位经济差'," \
                  "`damage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '伤害占比'," \
                  "`gold` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '经济占比')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_playerTable)  # 执行sql语句
    print("创建LPL2022春季赛player表成功，准备创建LPL2022春季赛hero表……")
except Exception as e:
    print("创建LPL2021春季赛player表失败：case%s" % e)

## LPL2022春季赛hero表
mycursor.execute('DROP TABLE IF EXISTS lpl2022SpringHero')
sql_heroTable = "CREATE TABLE `lpl2022SpringHero`  (`hrank` int(10) NULL COMMENT '排名'," \
                "`hero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci UNIQUE PRIMARY KEY COMMENT '英雄名'," \
                "`appearance` int(10) NULL DEFAULT NULL COMMENT '出场次数'," \
                "`pickRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pick比率'," \
                "`banRatio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ban率'," \
                "`winRate` varchar(20) CHARACTER  SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '胜率'," \
                "`totalKill_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总击杀（场均）'," \
                "`totalAssist_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总助攻（场均）'," \
                "`totalDie_perGame` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总死亡（场均）'," \
                "`killDieAssist` double(10, 2) NULL DEFAULT 0.00 COMMENT 'KDA'," \
                "`commonPlayers` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常用队员')"
try:  # 如果出现异常对异常处理
    # 执行SQL语句
    mycursor.execute(sql_heroTable)  # 执行sql语句
    print("创建LPL2022春季赛hero表成功")
except Exception as e:
    print("创建LPL2021春季赛player表失败：case%s" % e)
end = time.perf_counter()
print("所有数据表均已创建完成，耗时{:.3f}秒，准备进行LPL2020Spring~2022Spring数据获取与预处理……".format(end - start))

###################################################################################################################################################################################################
#########################################################################################  数据获取与预处理  #########################################################################################
start = time.perf_counter()  # 记录数据获取与预处理开始时间
## LPL2020春季赛team数据
# 数据获取
target_LPL2020teamApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_TEAMRANK_LIST_134_1_5.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_LPL2020teamApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
lpl2020springteamList = []
countTeam = 0
for i in tqdm(info_msg):  # 将进度条嵌入循环体输出
    team = i['sTeamName']  # 战队名
    appearance = i['iAppearancesFrequency']  # 出场次数
    win_lose = i['iWin'] + "/" + i['iLoss']  # 胜/负
    winRate = str(int(float(i['sAveragingWin'])))  # 胜率
    totalKill_perGame = i['iKill'] + "(" + str(round(float(i['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    catchEye_perGame = str(int(float(i['sAveragingWardPlaced'])))  # 场均插眼
    rowEye_perGame = str(int(float(i['sAveragingWardKilled'])))  # 场均排眼
    money_perGame = str(int(float(i['sAveragingGold'])))  # 场均金钱
    baron_perGame = str(round(float(i['sAveragingSmallDragon']), 1))  # 场均大龙
    dragon_perGame = str(round(float(i['sAveragingBigDragon']), 1))  # 场均小龙
    lpl2020springteamDict = {"team": team, "appearance": appearance, "win_lose": win_lose, "winRate": winRate,
                             "totalKill_perGame": totalKill_perGame,
                             "totalDie_perGame": totalDie_perGame, "catchEye_perGame": catchEye_perGame,
                             "rowEye_perGame": rowEye_perGame, "money_perGame": money_perGame,
                             "baron_perGame": baron_perGame,
                             "dragon_perGame": dragon_perGame}  # 将数据打包为字典格式
    lpl2020springteamList.append(lpl2020springteamDict)  # 利用循环，将每一个字典作为元素插入进列表中
    countTeam += 1
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
lpl2020springteamSet = pd.DataFrame(lpl2020springteamList)  # 将大列表转换为DataFrame
# 数据处理
lpl2020springteamSet.sort_values(by=['winRate'], inplace=True, ascending=False)  # 将DataFrame依据“胜率”列进行降序排序输出，并原地替换
lpl2020springteamSet = lpl2020springteamSet.reindex(columns=(
    ['trank', 'team', 'appearance', 'win_lose', 'winRate', 'totalKill_perGame', 'totalDie_perGame', 'catchEye_perGame',
     'rowEye_perGame', 'money_perGame', 'baron_perGame', 'dragon_perGame']))  # 在DataFrame首列增加一个空列
lpl2020springteamSet['trank'] = range(1, lpl2020springteamSet.shape[0] + 1)  # 为空列填充数据
# 写入数据
engine = create_engine(
    "mysql+pymysql://root:ShadowZed666@localhost:3306/LeagueofLegendsProLeague?charset=utf8mb4")  # 建立与本地MySQL数据库的连接
try:
    lpl2020springteamSet.to_sql('lpl2020springteam', con=engine, if_exists='append', index=False,
                                index_label=False)  # append为追加模式，index=False意为不将DataFrame的默认索引写入mysql表中
    sylpol.commit()  # 进行数据库提交，写入数据库
    print("{}条记录已写入lpl2020春季赛team表".format(countTeam))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('LPL2020春季赛team表数据写入失败')

## LPL2020春季赛player数据
# 数据获取
target_lpl2020playerApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_PERSONALRANK_LIST_134_1_5.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_lpl2020playerApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
lpl2020springplayerList = []
countPlayer = 0
for i in tqdm(info_msg):
    player = i['sMemberName']  # 队员
    position = i['iPosition']  # 位置
    appearance = int(i['iAppearancesFrequency'])  # 出场次数
    totalKill_perGame = int(i['iKill'])  # 总击杀（场均）
    totalAssist_perGame = i['iAssists'] + "(" + str(round(float(i['sAveragingAssists']), 1)) + ")"  # 总助攻（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    killDieAssist = round(float(i['iKDA']), 1)  # KDA
    money_perGame = int(float(i['sAveragingGold']))  # 场均金钱
    creepScore_perGame = int(float(i['sAveragingLastLasthit']))  # 场均补刀
    catchEye_perGame = int(float(i['sAveragingWardPlaced']))  # 场均插眼
    rowEye_perGame = int(float(i['sAveragingWardKilled']))  # 场均排眼
    attendanceRate_perGame = str(round(float(i['sAveragingOfferedRate']) * 100, 1))  # 场均参团率
    modelViewPresenter = int(i['iMVPFrequency'])  # MVP数
    lpl2020springplayerDict = {"player": player, "position": position, "appearance": appearance,
                               "totalKill_perGame": totalKill_perGame,
                               "totalAssist_perGame": totalAssist_perGame,
                               "totalDie_perGame": totalDie_perGame, "killDieAssist": killDieAssist,
                               "money_perGame": money_perGame, "creepScore_perGame": creepScore_perGame,
                               "catchEye_perGame": catchEye_perGame, "rowEye_perGame": rowEye_perGame,
                               "attendanceRate_perGame": attendanceRate_perGame,
                               "modelViewPresenter": modelViewPresenter}
    lpl2020springplayerList.append(lpl2020springplayerDict)
    countPlayer += 1
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
lpl2020springplayerSet = pd.DataFrame(lpl2020springplayerList)
# 数据处理
lpl2020springplayerSet.sort_values(by=['totalKill_perGame'], inplace=True, ascending=False)
lpl2020springplayerSet = lpl2020springplayerSet.reindex(
    columns=(['prank', 'player', 'position', 'appearance', 'totalKill_perGame',
              'totalAssist_perGame', 'totalDie_perGame', 'killDieAssist',
              'money_perGame', 'creepScore_perGame', 'catchEye_perGame',
              'rowEye_perGame', 'attendanceRate_perGame', 'modelViewPresenter']))
lpl2020springplayerSet['prank'] = range(1, lpl2020springplayerSet.shape[0] + 1)
lpl2020springplayerSet.set_index('prank')
index = 0
for s in info_msg:
    totalKill_perGame = s['iKill'] + "(" + str(round(float(s['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    lpl2020springplayerSet.loc[index, 'totalKill_perGame'] = totalKill_perGame  # 替换数据列
    index += 1
# 写入数据
try:
    lpl2020springplayerSet.to_sql('lpl2020springplayer', con=engine, if_exists='append', index=False,
                                  index_label=False)  # append为追加模式，index=False意为不将DataFrame的默认索引写入mysql表中
    sylpol.commit()  # 进行数据库提交，写入数据库
    print("{}条记录已写入lpl2020春季赛player表".format(countPlayer))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('2020春季赛player表数据写入失败')

## LPL2020春季赛hero数据
# 数据获取
target_lpl2020heroApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HERORANK_LIST_134_1_5.js'
target_lplHeroApi = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2755673'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_lpl2020heroApi, headers=headers)
response_lol = requests.get(url=target_lplHeroApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_lol = json.loads(response_lol.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
info_lol_msg = info_lol['hero']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
lpl2020springheroList = []
lpl2020springheroNameList = []
lplHeroIdList = [heroId['iChampionId'] for heroId in info_msg]
countHero = 0
for i in tqdm(info_msg):
    heroID = i['iChampionId']  # 英雄对应ID
    appearance = int(i['iAppearancesFrequency'])  # 出场次数
    pickRatio = int(float(i['sAveragingPick']) * 100)  # pick比率
    banRatio = str(int(float(i['sAveragingBan']) * 100))  # ban比率
    winRate = str(int(float(i['sAveragingWin']) * 100))  # 胜率
    totalKill_perGame = i['iKill'] + "(" + str(round(float(i['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    totalAssist_perGame = i['iAssists'] + "(" + str(round(float(i['sAveragingAssists']), 1)) + ")"  # 总助攻（场均）
    attendanceRate_perGame = str(round(float(i['sAveragingOfferedRate']) * 100, 1))  # 场均参团
    commonPlayers = i['sOftenMemberName']  # 常用队员
    heroDict = {"appearance": appearance, "pickRatio": pickRatio, "banRatio": banRatio, "winRate": winRate,
                "totalKill_perGame": totalKill_perGame, "totalDie_perGame": totalDie_perGame,
                "totalAssist_perGame": totalAssist_perGame,
                "attendanceRate_perGame": attendanceRate_perGame, "commonPlayers": commonPlayers}
    lpl2020springheroList.append(heroDict)
    countHero += 1
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
lpl2020springheroSet = pd.DataFrame(lpl2020springheroList)
# 数据处理
name = []
lpl2020springheroNameIdList = [i['heroId'] for i in info_lol_msg]  # 所有英雄对应的id
lpl2020springheroAllNamelist = [i['name'] for i in info_lol_msg]  # 所有英雄名字
for i in lplHeroIdList:
    for j in lpl2020springheroNameIdList:
        if i == j:
            # 由于从lpl数据页面无法获取到英雄名称，只能获取到对应的id
            # 一层循环是pick率前60的英雄id，二层是所有英雄的的id
            # 通过if判断，将LPL2020春季赛登场英雄写入到指定列表中
            name.append(lpl2020springheroAllNamelist[lpl2020springheroNameIdList.index(j)])
lpl2020springheroSet['hero'] = name
lpl2020springheroSet.sort_values(by=['pickRatio', 'appearance'], inplace=True, ascending=False)
lpl2020springheroSet = lpl2020springheroSet.reindex(columns=(['hrank', 'hero', 'appearance', 'pickRatio',
                                                              'banRatio', 'winRate', 'totalKill_perGame',
                                                              'totalDie_perGame', 'totalAssist_perGame',
                                                              'attendanceRate_perGame', 'commonPlayers']))
lpl2020springheroSet['hrank'] = range(1, lpl2020springheroSet.shape[0] + 1)
lpl2020springheroSet.set_index('hrank')
index = 0
for s in info_msg:
    pickRatio = str(int(float(s['sAveragingPick']) * 100))  # pick比率
    lpl2020springheroSet.loc[index, 'pickRatio'] = pickRatio
    index += 1
# 写入数据
try:
    lpl2020springheroSet.to_sql('lpl2020springhero', con=engine, if_exists='append', index=False,
                                index_label=False)  # append为追加模式，index=False意为不将DataFrame的默认索引写入mysql表中
    sylpol.commit()  # 进行数据库提交，写入数据库
    print("{}条记录已写入lpl2020春季赛hero表".format(countHero))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('2020春季赛hero表数据写入失败')

## LPL2020夏季赛team数据
# 数据获取
target_lpl2020teamApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_TEAMRANK_LIST_134_7_8.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_lpl2020teamApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
lpl2020summerteamList = []
countTeam = 0
for i in tqdm(info_msg):  # 将进度条嵌入循环体输出
    team = i['sTeamName']  # 战队名
    appearance = i['iAppearancesFrequency']  # 出场次数
    win_lose = i['iWin'] + "/" + i['iLoss']  # 胜/负
    winRate = str(int(float(i['sAveragingWin'])))  # 胜率
    totalKill_perGame = i['iKill'] + "(" + str(round(float(i['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    catchEye_perGame = str(int(float(i['sAveragingWardPlaced'])))  # 场均插眼
    rowEye_perGame = str(int(float(i['sAveragingWardKilled'])))  # 场均排眼
    money_perGame = str(int(float(i['sAveragingGold'])))  # 场均金钱
    baron_perGame = str(round(float(i['sAveragingSmallDragon']), 1))  # 场均大龙
    dragon_perGame = str(round(float(i['sAveragingBigDragon']), 1))  # 场均小龙
    lpl2020summerteamDict = {"team": team, "appearance": appearance, "win_lose": win_lose, "winRate": winRate,
                             "totalKill_perGame": totalKill_perGame,
                             "totalDie_perGame": totalDie_perGame, "catchEye_perGame": catchEye_perGame,
                             "rowEye_perGame": rowEye_perGame, "money_perGame": money_perGame,
                             "baron_perGame": baron_perGame,
                             "dragon_perGame": dragon_perGame}  # 将数据打包为字典格式
    lpl2020summerteamList.append(lpl2020summerteamDict)  # 利用循环，将每一个字典作为元素插入进列表中
    countTeam += 1
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
lpl2020summerteamSet = pd.DataFrame(lpl2020summerteamList)  # 将大列表转换为DataFrame
# 数据处理
lpl2020summerteamSet.sort_values(by=['winRate'], inplace=True, ascending=False)  # 将DataFrame依据“胜率”列进行降序排序输出，并原地替换
lpl2020summerteamSet = lpl2020summerteamSet.reindex(columns=(
    ['trank', 'team', 'appearance', 'win_lose', 'winRate', 'totalKill_perGame', 'totalDie_perGame', 'catchEye_perGame',
     'rowEye_perGame', 'money_perGame', 'baron_perGame', 'dragon_perGame']))  # 在DataFrame首列增加一个空列
lpl2020summerteamSet['trank'] = range(1, lpl2020summerteamSet.shape[0] + 1)  # 为空列填充数据
# 写入数据
try:
    lpl2020summerteamSet.to_sql('lpl2020summerteam', con=engine, if_exists='append', index=False,
                                index_label=False)  # append为追加模式，index=False意为不将DataFrame的默认索引写入mysql表中
    sylpol.commit()  # 进行数据库提交，写入数据库
    print("{}条记录已写入lpl2020夏季赛team表".format(countTeam))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('2020夏季赛team表数据写入失败')

## LPL2020夏季赛player数据
# 数据获取
target_lpl2020playerApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_PERSONALRANK_LIST_134_7_8.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_lpl2020playerApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
countPlayer = 0
lpl2020summerplayerList = []
for i in tqdm(info_msg):
    player = i['sMemberName']  # 队员
    position = i['iPosition']  # 位置
    appearance = int(i['iAppearancesFrequency'])  # 出场次数
    totalKill_perGame = int(i['iKill'])  # 总击杀（场均）
    totalAssist_perGame = i['iAssists'] + "(" + str(round(float(i['sAveragingAssists']), 1)) + ")"  # 总助攻（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    killDieAssist = round(float(i['iKDA'] + "0"), 1)  # KDA
    money_perGame = int(float(i['sAveragingGold']))  # 场均金钱
    creepScore_perGame = int(float(i['sAveragingLastLasthit']))  # 场均补刀
    catchEye_perGame = int(float(i['sAveragingWardPlaced']))  # 场均插眼
    rowEye_perGame = int(float(i['sAveragingWardKilled']))  # 场均排眼
    attendanceRate_perGame = str(round(float(i['sAveragingOfferedRate']) * 100, 1))  # 场均参团率
    modelViewPresenter = int(i['iMVPFrequency'])  # MVP数
    lpl2020summerplayerDict = {"player": player, "position": position, "appearance": appearance,
                               "totalKill_perGame": totalKill_perGame, "totalAssist_perGame": totalAssist_perGame,
                               "totalDie_perGame": totalDie_perGame, "killDieAssist": killDieAssist,
                               "money_perGame": money_perGame, "creepScore_perGame": creepScore_perGame,
                               "catchEye_perGame": catchEye_perGame, "rowEye_perGame": rowEye_perGame,
                               "attendanceRate_perGame": attendanceRate_perGame,
                               "modelViewPresenter": modelViewPresenter}
    lpl2020summerplayerList.append(lpl2020summerplayerDict)
    countPlayer += 1
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
lpl2020summerplayerSet = pd.DataFrame(lpl2020summerplayerList)
# 数据处理
lpl2020summerplayerSet.sort_values(by=['totalKill_perGame'], inplace=True, ascending=False)
lpl2020summerplayerSet = lpl2020summerplayerSet.reindex(
    columns=(['prank', 'player', 'position', 'appearance', 'totalKill_perGame',
              'totalAssist_perGame', 'totalDie_perGame', 'killDieAssist',
              'money_perGame', 'creepScore_perGame', 'catchEye_perGame',
              'rowEye_perGame', 'attendanceRate_perGame', 'modelViewPresenter']))
lpl2020summerplayerSet['prank'] = range(1, lpl2020summerplayerSet.shape[0] + 1)
lpl2020summerplayerSet.set_index('prank')
index = 0
for s in info_msg:
    totalKill_perGame = s['iKill'] + "(" + str(round(float(s['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    lpl2020summerplayerSet.loc[index, 'totalKill_perGame'] = totalKill_perGame
    index += 1
# 写入数据
try:
    lpl2020summerplayerSet.to_sql('lpl2020summerplayer', con=engine, if_exists='append', index=False, index_label=False)
    sylpol.commit()  # 进行数据库提交，写入数据库
    print("{}条记录已写入lpl2020夏季赛player表".format(countPlayer))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('2020夏季赛player表数据写入失败')

## LPL2020夏季赛hero数据
# 数据获取
target_lpl2020heroApi = 'https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HERORANK_LIST_134_7_8.js'
target_lplHeroApi = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2755673'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
response = requests.get(url=target_lpl2020heroApi, headers=headers)
response_lol = requests.get(url=target_lplHeroApi, headers=headers)
# 数据解析
info = json.loads(response.text)  # 将str对象转换为dict（字典）对象
info_lol = json.loads(response_lol.text)  # 将str对象转换为dict（字典）对象
info_msg = info['msg']  # 使用字典里面的键获取对于的值
info_lol_msg = info_lol['hero']  # 使用字典里面的键获取对于的值
# 数据选择丨数据预处理
lpl2020summerheroList = []
lpl2020summerheroNameList = []
lplHeroIdList = [heroId['iChampionId'] for heroId in info_msg]
countHero = 0
for i in tqdm(info_msg):
    heroID = i['iChampionId']  # 英雄对应ID
    appearance = int(i['iAppearancesFrequency'])  # 出场次数
    pickRatio = int(float(i['sAveragingPick']) * 100)  # pick比率
    banRatio = str(int(float(i['sAveragingBan']) * 100))  # ban比率
    winRate = str(int(float(i['sAveragingWin']) * 100))  # 胜率
    totalKill_perGame = i['iKill'] + "(" + str(round(float(i['sAveragingKill']), 1)) + ")"  # 总击杀（场均）
    totalDie_perGame = i['iDeath'] + "(" + str(round(float(i['sAveragingDeath']), 1)) + ")"  # 总死亡（场均）
    totalAssist_perGame = i['iAssists'] + "(" + str(round(float(i['sAveragingAssists']), 1)) + ")"  # 总助攻（场均）
    attendanceRate_perGame = str(round(float(i['sAveragingOfferedRate']) * 100, 1))  # 场均参团
    commonPlayers = i['sOftenMemberName']  # 常用队员
    lpl2020summerheroDict = {"appearance": appearance, "pickRatio": pickRatio, "banRatio": banRatio, "winRate": winRate,
                             "totalKill_perGame": totalKill_perGame, "totalDie_perGame": totalDie_perGame,
                             "totalAssist_perGame": totalAssist_perGame,
                             "attendanceRate_perGame": attendanceRate_perGame, "commonPlayers": commonPlayers}
    lpl2020summerheroList.append(lpl2020summerheroDict)
    countHero += 1
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
lpl2020summerheroSet = pd.DataFrame(lpl2020summerheroList)
# 数据处理
name = []
lpl2020summerheroNameIdList = [i['heroId'] for i in info_lol_msg]  # 所有英雄对应的id
lpl2020summerheroAllNamelist = [i['name'] for i in info_lol_msg]  # 所有英雄名字
for i in lplHeroIdList:
    for j in lpl2020summerheroNameIdList:
        if i == j:
            # 由于从lpl数据页面无法获取到英雄名称，只能获取到对应的id
            # 一层循环是pick率前60的英雄id，二层是所有英雄的的id
            # 通过if判断，将LPL2020春季赛登场英雄写入到指定列表中
            name.append(lpl2020summerheroAllNamelist[lpl2020summerheroNameIdList.index(j)])
lpl2020summerheroSet['hero'] = name
lpl2020summerheroSet.sort_values(by=['pickRatio', 'appearance'], inplace=True, ascending=False)
lpl2020summerheroSet = lpl2020summerheroSet.reindex(columns=(['hrank', 'hero', 'appearance', 'pickRatio',
                                                              'banRatio', 'winRate', 'totalKill_perGame',
                                                              'totalDie_perGame', 'totalAssist_perGame',
                                                              'attendanceRate_perGame', 'commonPlayers']))
lpl2020summerheroSet['hrank'] = range(1, lpl2020summerheroSet.shape[0] + 1)
lpl2020summerheroSet.set_index('hrank')
index = 0
for s in info_msg:
    pickRatio = str(int(float(s['sAveragingPick']) * 100))  # pick比率
    lpl2020summerheroSet.loc[index, 'pickRatio'] = pickRatio
    index += 1
# 写入数据
try:
    sylpol.commit()  # 进行数据库提交，写入数据库
    lpl2020summerheroSet.to_sql('lpl2020summerhero', con=engine, if_exists='append', index=False, index_label=False)
    print("{}条记录已写入lpl2020夏季赛hero表".format(countHero))
except:
    sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    print('2020夏季赛hero表数据写入失败')

## LPL2021春季赛team数据
## 使用selenium控制edge浏览器
edgedriver = Service('./msedgedriver')  # 调用edge浏览器驱动程序
edgedriver.start()  # 打开浏览器
browers = webdriver.Remote(edgedriver.service_url)
# 数据获取
target_url = "https://lpl.qq.com"
browers.get(target_url)
time.sleep(1)
heroButton = browers.find_element(By.LINK_TEXT, "数据")  # link_text用于定位a标签，参数规则为字符全匹配
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
heroButton = browers.find_element(By.LINK_TEXT, "2021赛季")  # link_text用于定位a标签，参数规则为字符全匹配
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
heroButton = browers.find_element(By.XPATH, "/html/body/div[4]/div/ul/li[1]/a/img")  # xpath用于定位精确标签
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
windows = browers.window_handles  # 获取父页面的句柄，为页面切换做准备
browers.switch_to.window(windows[-1])  # switch_to.window()方法用于新旧窗口之间的切换  ## 控制浏览器将窗口切换为第-1个页面
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-1'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'teamRank'})
tr = tbody.find_all('tr')
countTeam = 0  # team记录计数器
lpl2021springteamList = []
for j in tqdm(tr):
    trank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    team = j.find_all('td')[1].get_text()  # 战队名
    appearance = j.find('b').get_text()  # 出场次数
    win_lose = j.find_all('b')[1].get_text()  # 胜/负
    winRate = j.find_all('b')[2].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalDie_perGame = j.find_all('b')[4].get_text()  # 总死亡（场均）
    catchEye_perGame = j.find_all('b')[5].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[6].get_text()  # 场均排眼
    money_perGame = j.find_all('td')[9].get_text()  # 场均金钱
    baron_perGame = j.find_all('b')[7].get_text()  # 场均大龙
    dragon_perGame = j.find_all('b')[-1].get_text()  # 场均小龙
    lpl2021springteamDict = {'trank': trank, 'team': team, 'appearance': appearance, 'win_lose': win_lose,
                             'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalDie_perGame': totalDie_perGame, 'catchEye_perGame': catchEye_perGame,
                             'rowEye_perGame': rowEye_perGame, 'money_perGame': money_perGame,
                             'baron_perGame': baron_perGame, 'dragon_perGame': dragon_perGame}
    lpl2021springteamList.append(lpl2021springteamDict)
    # 写入数据
    sql_teamInsert = 'insert into lpl2021SpringTeam (trank, team, appearance, Win_lose, winRate, totalKill_perGame, totalDie_perGame, catchEye_perGame, ' \
                     'rowEye_perGame, money_perGame, baron_perGame, dragon_perGame)' \
                     'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        trank, team, appearance, win_lose, winRate, totalKill_perGame, totalDie_perGame, catchEye_perGame,
        rowEye_perGame, money_perGame, baron_perGame, dragon_perGame)  # 向team表中插入数据
    try:
        mycursor.execute(sql_teamInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countTeam += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021春季赛team表数据写入失败')
lpl2021springteamSet = pd.DataFrame(lpl2021springteamList)

print("{}条记录已写入lpl2021春季赛team表".format(countTeam))
## LPL2021春季赛player数据
# 数据获取
heroButton = browers.find_element(By.LINK_TEXT, "个人数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-2'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'playerRank'})
tr = tbody.find_all('tr')
countPlayer = 0
lpl2021springplayerList = []
for j in tqdm(tr):
    prank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    player = j.find_all('td')[1].get_text()  # 选手名
    position = j.find('b').get_text()  # 位置
    appearance = j.find_all('b')[1].get_text()  # 出场次数
    modelViewPresenter = j.find_all('b')[2].get_text()  # MVP次数
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[4].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[5].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[6].get_text()  # KDA
    money_perGame = j.find_all('b')[7].get_text()  # 场均金钱
    creepScore_perGame = j.find_all('td')[10].get_text()  # 场均补刀
    catchEye_perGame = j.find_all('b')[8].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[9].get_text()  # 场均排眼
    attendanceRate_perGame = j.find_all('b')[10].get_text()  # 场均参团率
    contrapositionEconomicDifference = j.find_all('b')[11].get_text()  # 场均对位经济差
    damage = j.find_all('b')[12].get_text()  # 伤害占比
    gold = j.find_all('b')[13].get_text()  # 经济占比
    lpl2021springplayerDict = {'prank': prank, 'player': player, 'appearance': appearance,
                               'modelViewPresenter': modelViewPresenter, 'totalKill_perGame': totalKill_perGame,
                               'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                               'killDieAssist': killDieAssist, 'money_perGame': money_perGame,
                               'creepScore_perGame': creepScore_perGame, 'catchEye_perGame': catchEye_perGame,
                               'rowEye_perGame': rowEye_perGame,
                               'attendanceRate_perGame': attendanceRate_perGame,
                               'contrapositionEconomicDifference': contrapositionEconomicDifference, 'damage': damage,
                               'gold': gold}
    lpl2021springplayerList.append(lpl2021springplayerDict)
    # 写入数据
    sql_playerInsert = 'insert into lpl2021SpringPlayer(prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame, ' \
                       'totalDie_perGame, killDieAssist, money_perGame, creepScore_perGame, catchEye_perGame, rowEye_perGame, attendanceRate_perGame, ' \
                       'contrapositionEconomicDifference, damage, gold) ' \
                       'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame,
        totalDie_perGame, killDieAssist, money_perGame,
        creepScore_perGame, catchEye_perGame, rowEye_perGame, attendanceRate_perGame, contrapositionEconomicDifference,
        damage, gold)  # 向player表中插入数据
    try:
        mycursor.execute(sql_playerInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countPlayer += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021春季赛player表数据写入失败')
lpl2021springplayerSet = pd.DataFrame(lpl2021springplayerList)
print("{}条记录已写入lpl2021春季赛player表".format(countPlayer))

## LPL2021春季赛hero数据
# 数据获取
heroButton = browers.find_element(By.LINK_TEXT, "英雄数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-3'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'heroRank'})
tr = tbody.find_all('tr')
countHero = 0
lpl2021springheroList = []
for j in tqdm(tr):
    hrank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    hero = j.find_all('td')[1].get_text()  # 英雄名
    appearance = j.find('b').get_text()  # 出场次数
    pickRatio = j.find_all('b')[1].get_text()  # pick比率
    banRatio = j.find_all('b')[2].get_text()  # ban率
    winRate = j.find_all('b')[3].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[4].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[5].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[6].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[7].get_text()  # KDA
    commonPlayers = j.find_all('b')[8].get_text()  # 常用队员
    lpl2021springheroDict = {'hrank': hrank, 'hero': hero, 'appearance': appearance, 'pickRatio': pickRatio,
                             'banRatio': banRatio, 'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                             'killDieAssist': killDieAssist, 'commonPlayers': commonPlayers}
    lpl2021springheroList.append(lpl2021springheroDict)
    # 写入数据
    sql_heroInsert = 'insert into lpl2021SpringHero(hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame, totalDie_perGame, killDieAssist, commonPlayers) ' \
                     'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame, totalDie_perGame,
        killDieAssist, commonPlayers)  # 向hero表中插入数据
    try:
        mycursor.execute(sql_heroInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countHero += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021春季赛hero表数据写入失败')
lpl2021springheroSet = pd.DataFrame(lpl2021springheroList)
print("{}条记录已写入lpl2021春季赛hero表".format(countHero))

## LPL2021夏季赛team数据
# 数据获取
heroButton = browers.find_element(By.LINK_TEXT, "数据")  # link_text用于定位a标签，参数规则为字符全匹配
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
heroButton = browers.find_element(By.LINK_TEXT, "2021赛季")  # link_text用于定位a标签，参数规则为字符全匹配
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
heroButton = browers.find_element(By.XPATH, "/html/body/div[4]/div/ul/li[2]/a/img")  # xpath用于定位精确标签
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
windows = browers.window_handles  # 获取父页面的句柄，为页面切换做准备
browers.switch_to.window(windows[-1])  # switch_to.window()方法用于新旧窗口之间的切换  ## 控制浏览器将窗口切换为第-1个页面
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-1'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'teamRank'})
tr = tbody.find_all('tr')
countTeam = 0  # team记录计数器
lpl2021summerteamList = []
for j in tqdm(tr):
    trank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    team = j.find_all('td')[1].get_text()  # 战队名
    appearance = j.find('b').get_text()  # 出场次数
    win_lose = j.find_all('b')[1].get_text()  # 胜/负
    winRate = j.find_all('b')[2].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalDie_perGame = j.find_all('b')[4].get_text()  # 总死亡（场均）
    catchEye_perGame = j.find_all('b')[5].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[6].get_text()  # 场均排眼
    money_perGame = j.find_all('td')[9].get_text()  # 场均金钱
    baron_perGame = j.find_all('b')[7].get_text()  # 场均大龙
    dragon_perGame = j.find_all('b')[-1].get_text()  # 场均小龙
    lpl2021summerteamDict = {'trank': trank, 'team': team, 'appearance': appearance, 'win_lose': win_lose,
                             'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalDie_perGame': totalDie_perGame, 'catchEye_perGame': catchEye_perGame,
                             'rowEye_perGame': rowEye_perGame, 'money_perGame': money_perGame,
                             'baron_perGame': baron_perGame, 'dragon_perGame': dragon_perGame}
    lpl2021summerteamList.append(lpl2021summerteamDict)
    # 写入数据
    sql_teamInsert = 'insert into lpl2021summerteam (trank, team, appearance, Win_lose, winRate, totalKill_perGame, totalDie_perGame, ' \
                     'catchEye_perGame, rowEye_perGame, money_perGame, baron_perGame, dragon_perGame) ' \
                     'values(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        trank, team, appearance, win_lose, winRate, totalKill_perGame, totalDie_perGame, catchEye_perGame,
        rowEye_perGame, money_perGame, baron_perGame, dragon_perGame)  # 向team表中插入数据
    try:
        mycursor.execute(sql_teamInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countTeam += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021夏季赛team表数据写入失败')
lpl2021summerteamSet = pd.DataFrame(lpl2021summerteamList)
print("{}条记录已写入lpl2021夏季赛team表".format(countTeam))

## LPL2021夏季赛player数据
# 数据获取
time.sleep(2)
heroButton = browers.find_element(By.LINK_TEXT, "个人数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-2'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'playerRank'})
tr = tbody.find_all('tr')
countPlayer = 0
lpl2021summerplayerList = []
for j in tqdm(tr):
    prank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    player = j.find_all('td')[1].get_text()  # 选手名
    position = j.find('b').get_text()  # 位置
    appearance = j.find_all('b')[1].get_text()  # 出场次数
    modelViewPresenter = j.find_all('b')[2].get_text()  # MVP次数
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[4].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[5].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[6].get_text()  # KDA
    money_perGame = j.find_all('b')[7].get_text()  # 场均金钱
    creepScore_perGame = j.find_all('td')[10].get_text()  # 场均补刀
    catchEye_perGame = j.find_all('b')[8].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[9].get_text()  # 场均排眼
    attendanceRate_perGame = j.find_all('b')[10].get_text()  # 场均参团率
    contrapositionEconomicDifference = j.find_all('b')[11].get_text()  # 场均对位经济差
    damage = j.find_all('b')[12].get_text()  # 伤害占比
    gold = j.find_all('b')[13].get_text()  # 经济占比
    lpl2021summerplayerDict = {'prank': prank, 'player': player, 'appearance': appearance,
                               'modelViewPresenter': modelViewPresenter, 'totalKill_perGame': totalKill_perGame,
                               'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                               'killDieAssist': killDieAssist, 'money_perGame': money_perGame,
                               'creepScore_perGame': creepScore_perGame, 'catchEye_perGame': catchEye_perGame,
                               'rowEye_perGame': rowEye_perGame, 'attendanceRate_perGame': attendanceRate_perGame,
                               'contrapositionEconomicDifference': contrapositionEconomicDifference, 'damage': damage,
                               'gold': gold}
    lpl2021summerplayerList.append(lpl2021summerplayerDict)
    # 写入数据
    sql_playerInsert = 'insert into lpl2021summerplayer(prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame, totalDie_perGame, killDieAssist, ' \
                       'money_perGame, creepScore_perGame, catchEye_perGame, rowEye_perGame, attendanceRate_perGame, contrapositionEconomicDifference, damage, gold) ' \
                       'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame,
        totalDie_perGame, killDieAssist, money_perGame, creepScore_perGame, catchEye_perGame,
        rowEye_perGame, attendanceRate_perGame, contrapositionEconomicDifference, damage, gold)  # 向player表中插入数据
    try:
        mycursor.execute(sql_playerInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countPlayer += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021夏季赛player表数据写入失败')
lpl2021summerplayerSet = pd.DataFrame(lpl2021summerplayerList)
print("{}条记录已写入lpl2021夏季赛player表".format(countPlayer))

## LPL2021夏季赛hero数据
# 数据获取
heroButton = browers.find_element(By.LINK_TEXT, "英雄数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-3'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'heroRank'})
tr = tbody.find_all('tr')
countHero = 0
lpl2021summerheroList = []
for j in tqdm(tr):
    hrank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    hero = j.find_all('td')[1].get_text()  # 英雄名
    appearance = j.find('b').get_text()  # 出场次数
    pickRatio = j.find_all('b')[1].get_text()  # pick比率
    banRatio = j.find_all('b')[2].get_text()  # ban率
    winRate = j.find_all('b')[3].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[4].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[5].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[6].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[7].get_text()  # KDA
    commonPlayers = j.find_all('b')[8].get_text()  # 常用队员
    lpl2021summerheroDict = {'hrank': hrank, 'hero': hero, 'appearance': appearance, 'pickRatio': pickRatio,
                             'banRatio': banRatio, 'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                             'killDieAssist': killDieAssist, 'commonPlayers': commonPlayers}
    lpl2021summerheroList.append(lpl2021summerheroDict)
    # 写入数据
    sql_heroInsert = 'insert into lpl2021summerhero(hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame, totalDie_perGame, killDieAssist, commonPlayers) ' \
                     'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame,
        totalDie_perGame, killDieAssist, commonPlayers)  # 向hero表中插入数据
    try:
        mycursor.execute(sql_heroInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countHero += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2021夏季赛hero表数据写入失败')
lpl2021summerheroSet = pd.DataFrame(lpl2021summerheroList)
print("{}条记录已写入lpl2021夏季赛hero表".format(countHero))

## LPL2022春季赛team数据
# 数据获取
heroButton = browers.find_element(By.LINK_TEXT, "数据")  # link_text用于定位a标签，参数规则为字符全匹配
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
heroButton = browers.find_element(By.XPATH, "/html/body/div[4]/div/ul/li/a/img")  # xpath用于定位精确标签
heroButton.click()  # 控制浏览器鼠标左键单击该定位
time.sleep(2)  # 停留几秒，用于点击后稳定页面
windows = browers.window_handles  # 获取父页面的句柄，为页面切换做准备
browers.switch_to.window(windows[-1])  # switch_to.window()方法用于新旧窗口之间的切换  ## 控制浏览器将窗口切换为第-1个页面
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-1'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'teamRank'})
tr = tbody.find_all('tr')
lpl2022springteamList = []
countTeam = 0  # team记录计数器
for j in tqdm(tr):
    trank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    team = j.find_all('td')[1].get_text()  # 战队名
    appearance = j.find('b').get_text()  # 出场次数
    win_lose = j.find_all('b')[1].get_text()  # 胜/负
    winRate = j.find_all('b')[2].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalDie_perGame = j.find_all('b')[4].get_text()  # 总死亡（场均）
    catchEye_perGame = j.find_all('b')[5].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[6].get_text()  # 场均排眼
    money_perGame = j.find_all('td')[9].get_text()  # 场均金钱
    baron_perGame = j.find_all('b')[7].get_text()  # 场均大龙
    dragon_perGame = j.find_all('b')[-1].get_text()  # 场均小龙
    lpl2022springteamDict = {'trank': trank, 'team': team, 'appearance': appearance, 'win_lose': win_lose,
                             'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalDie_perGame': totalDie_perGame, 'catchEye_perGame': catchEye_perGame,
                             'rowEye_perGame': rowEye_perGame, 'money_perGame': money_perGame,
                             'baron_perGame': baron_perGame, 'dragon_perGame': dragon_perGame}
    lpl2022springteamList.append(lpl2022springteamDict)
    # 写入数据
    sql_teamInsert = 'insert into lpl2022SpringTeam (trank, team, appearance, Win_lose, winRate, totalKill_perGame, totalDie_perGame, catchEye_perGame, ' \
                     'rowEye_perGame, money_perGame, baron_perGame, dragon_perGame)' \
                     'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        trank, team, appearance, win_lose, winRate, totalKill_perGame, totalDie_perGame, catchEye_perGame,
        rowEye_perGame, money_perGame, baron_perGame, dragon_perGame)  # 向team表中插入数据
    try:
        mycursor.execute(sql_teamInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countTeam += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2022春季赛team表数据写入失败')
lpl2022springteamSet = pd.DataFrame(lpl2022springteamList)
print("{}条记录已写入lpl2022春季赛team表".format(countTeam))

## LPL2022春季赛player数据
# 数据获取
time.sleep(2)
heroButton = browers.find_element(By.LINK_TEXT, "个人数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-2'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'playerRank'})
tr = tbody.find_all('tr')
countPlayer = 0
lpl2022springplayerList = []
for j in tqdm(tr):
    prank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    player = j.find_all('td')[1].get_text()  # 选手名
    position = j.find('b').get_text()  # 位置
    appearance = j.find_all('b')[1].get_text()  # 出场次数
    modelViewPresenter = j.find_all('b')[2].get_text()  # MVP次数
    totalKill_perGame = j.find_all('b')[3].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[4].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[5].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[6].get_text()  # KDA
    money_perGame = j.find_all('b')[7].get_text()  # 场均金钱
    creepScore_perGame = j.find_all('td')[10].get_text()  # 场均补刀
    catchEye_perGame = j.find_all('b')[8].get_text()  # 场均插眼
    rowEye_perGame = j.find_all('b')[9].get_text()  # 场均排眼
    attendanceRate_perGame = j.find_all('b')[10].get_text()  # 场均参团率
    contrapositionEconomicDifference = j.find_all('b')[11].get_text()  # 场均对位经济差
    damage = j.find_all('b')[12].get_text()  # 伤害占比
    gold = j.find_all('b')[13].get_text()  # 经济占比
    lpl2022springplayerDict = {'prank': prank, 'player': player, 'appearance': appearance,
                               'modelViewPresenter': modelViewPresenter, 'totalKill_perGame': totalKill_perGame,
                               'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                               'killDieAssist': killDieAssist, 'money_perGame': money_perGame,
                               'creepScore_perGame': creepScore_perGame, 'catchEye_perGame': catchEye_perGame,
                               'rowEye_perGame': rowEye_perGame, 'attendanceRate_perGame': attendanceRate_perGame,
                               'contrapositionEconomicDifference': contrapositionEconomicDifference, 'damage': damage,
                               'gold': gold}
    lpl2022springplayerList.append(lpl2022springplayerDict)
    # 写入数据
    sql_playerInsert = 'insert into lpl2022SpringPlayer(prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame, totalDie_perGame, killDieAssist, ' \
                       'money_perGame, creepScore_perGame, catchEye_perGame, rowEye_perGame, attendanceRate_perGame, contrapositionEconomicDifference, damage, gold) ' \
                       'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        prank, player, position, appearance, modelViewPresenter, totalKill_perGame, totalAssist_perGame,
        totalDie_perGame, killDieAssist, money_perGame, creepScore_perGame, catchEye_perGame,
        rowEye_perGame, attendanceRate_perGame, contrapositionEconomicDifference, damage, gold)  # 向player表中插入数据
    try:
        mycursor.execute(sql_playerInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countPlayer += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2022春季赛player表数据写入失败')
lpl2022springplayerSet = pd.DataFrame(lpl2022springplayerList)
print("{}条记录已写入lpl2022春季赛player表".format(countPlayer))

## LPL2022春季赛hero数据
# 数据获取
time.sleep(2)
heroButton = browers.find_element(By.LINK_TEXT, "英雄数据")
heroButton.click()
time.sleep(2)
# 数据解析
page_source = browers.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 数据选择丨数据预处理
div1 = soup.find('div', attrs={'class': 'event-wrap wp'})
div2 = div1.find('div', attrs={'class': 'event event-3'})
div3 = div2.find('div', attrs={'class': 'table-wrap wp'})
div4 = div3.find('div', attrs={'class': 'table-box wb'})
table = div4.find('table', attrs={'class': 'table'})
tbody = table.find('tbody', attrs={'id': 'heroRank'})
tr = tbody.find_all('tr')
countHero = 0
lpl2022springheroList = []
for j in tqdm(tr):
    hrank = j.find('span', attrs={'class': 'db data-spr'}).get_text()  # 排名
    hero = j.find_all('td')[1].get_text()  # 英雄名
    appearance = j.find('b').get_text()  # 出场次数
    pickRatio = j.find_all('b')[1].get_text()  # pick比率
    banRatio = j.find_all('b')[2].get_text()  # ban率
    winRate = j.find_all('b')[3].get_text()  # 胜率
    totalKill_perGame = j.find_all('b')[4].get_text()  # 总击杀（场均）
    totalAssist_perGame = j.find_all('b')[5].get_text()  # 总助攻（场均）
    totalDie_perGame = j.find_all('b')[6].get_text()  # 总死亡（场均）
    killDieAssist = j.find_all('b')[7].get_text()  # KDA
    commonPlayers = j.find_all('b')[8].get_text()  # 常用队员
    lpl2022springheroDict = {'hrank': hrank, 'hero': hero, 'appearance': appearance, 'pickRatio': pickRatio,
                             'banRatio': banRatio, 'winRate': winRate, 'totalKill_perGame': totalKill_perGame,
                             'totalAssist_perGame': totalAssist_perGame, 'totalDie_perGame': totalDie_perGame,
                             'killDieAssist': killDieAssist, 'commonPlayers': commonPlayers}
    lpl2022springheroList.append(lpl2022springheroDict)
    # 写入数据
    sql_heroInsert = 'insert into lpl2022SpringHero(hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame, totalDie_perGame, killDieAssist, commonPlayers) ' \
                     'values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
        hrank, hero, appearance, pickRatio, banRatio, winRate, totalKill_perGame, totalAssist_perGame,
        totalDie_perGame, killDieAssist, commonPlayers)  # 向hero表中插入数据
    try:
        mycursor.execute(sql_heroInsert)
        sylpol.commit()  # 进行数据库提交，写入数据库
        countHero += 1
    except:
        sylpol.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
        print('lpl2022春季赛hero表数据写入失败')
lpl2022springheroSet = pd.DataFrame(lpl2022springheroList)
print("{}条记录已写入lpl2022春季赛hero表".format(countHero))
end = time.perf_counter()  # 记录数据获取与预处理结束时间

###################################################################################################################################################################################################
########################################################################################  关闭数据库连接  #########################################################################################
mycursor.close()
sylpol.close()
print('LPL2020Spring~2022Spring数据采集、预处理已完成！数据库连接已关闭，共计耗时{:.3f}秒'.format(end - start))


###################################################################################################################################################################################################
#########################################################################################  数据清洗与写入  ##########################################################################################
start = time.perf_counter()  # 记录数据清洗与写入开始时间
lpl2020springteamSet['totalKill_perGame'] = lpl2020springteamSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020springteamSet['totalDie_perGame'] = lpl2020springteamSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020springplayerSet['totalKill_perGame'] = lpl2020springplayerSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020springplayerSet['totalAssist_perGame'] = lpl2020springplayerSet['totalAssist_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020springplayerSet['totalDie_perGame'] = lpl2020springplayerSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))

lpl2020summerteamSet['totalKill_perGame'] = lpl2020summerteamSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020summerteamSet['totalDie_perGame'] = lpl2020summerteamSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020summerplayerSet['totalKill_perGame'] = lpl2020summerplayerSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020summerplayerSet['totalAssist_perGame'] = lpl2020summerplayerSet['totalAssist_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2020summerplayerSet['totalDie_perGame'] = lpl2020summerplayerSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))

lpl2021springteamSet['winRate'] = lpl2021springteamSet['winRate'].apply(lambda x: re.sub('%', "", x))
lpl2021springteamSet['totalKill_perGame'] = lpl2021springteamSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021springteamSet['totalDie_perGame'] = lpl2021springteamSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021springplayerSet['totalKill_perGame'] = lpl2021springplayerSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021springplayerSet['totalAssist_perGame'] = lpl2021springplayerSet['totalAssist_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021springplayerSet['totalDie_perGame'] = lpl2021springplayerSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))

lpl2021summerteamSet['winRate'] = lpl2021summerteamSet['winRate'].apply(lambda x: re.sub('%', "", x))
lpl2021summerteamSet['totalKill_perGame'] = lpl2021summerteamSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021summerteamSet['totalDie_perGame'] = lpl2021summerteamSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021summerplayerSet['totalKill_perGame'] = lpl2021summerplayerSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021summerplayerSet['totalAssist_perGame'] = lpl2021summerplayerSet['totalAssist_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2021summerplayerSet['totalDie_perGame'] = lpl2021summerplayerSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))

lpl2022springteamSet['winRate'] = lpl2022springteamSet['winRate'].apply(lambda x: re.sub('%', "", x))
lpl2022springteamSet['totalKill_perGame'] = lpl2022springteamSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2022springteamSet['totalDie_perGame'] = lpl2022springteamSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2022springplayerSet['totalKill_perGame'] = lpl2022springplayerSet['totalKill_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2022springplayerSet['totalAssist_perGame'] = lpl2022springplayerSet['totalAssist_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))
lpl2022springplayerSet['totalDie_perGame'] = lpl2022springplayerSet['totalDie_perGame'].apply(lambda x: re.sub('\(.*?\)', "", x))

# 将DataFrame写入xlsx文件，以备后续数据分析与数据可视化使用
lpl2020springteamSet.to_excel('LPL2020春季赛team数据.xlsx', index=False)
lpl2020springplayerSet.to_excel('LPL2020春季赛player数据.xlsx', index=False)
lpl2020springheroSet.to_excel('LPL2020春季赛hero数据.xlsx', index=False)
lpl2020summerteamSet.to_excel('LPL2020夏季赛team数据.xlsx', index=False)
lpl2020summerplayerSet.to_excel('LPL2020夏季赛player数据.xlsx', index=False)
lpl2020summerheroSet.to_excel('LPL2020夏季赛hero数据.xlsx', index=False)
lpl2021springteamSet.to_excel('LPL2021春季赛team数据.xlsx', index=False)
lpl2021springplayerSet.to_excel('LPL2021春季赛player数据.xlsx', index=False)
lpl2021springheroSet.to_excel('LPL2021春季赛hero数据.xlsx', index=False)
lpl2021summerteamSet.to_excel('LPL2021夏季赛team数据.xlsx', index=False)
lpl2021summerplayerSet.to_excel('LPL2021夏季赛player数据.xlsx', index=False)
lpl2021summerheroSet.to_excel('LPL2021夏季赛hero数据.xlsx', index=False)
lpl2022springteamSet.to_excel('LPL2022春季赛team数据.xlsx', index=False)
lpl2022springplayerSet.to_excel('LPL2022春季赛player数据.xlsx', index=False)
lpl2022springheroSet.to_excel('LPL2022春季赛hero数据.xlsx', index=False)

# 将DataFrame写入csv文件，以备后续提交使用
lpl2020springteamSet.to_csv('LPL2020春季赛team数据.csv', index=False)
lpl2020springplayerSet.to_csv('LPL2020春季赛player数据.csv', index=False)
lpl2020springheroSet.to_csv('LPL2020春季赛hero数据.csv', index=False)
lpl2020summerteamSet.to_csv('LPL2020夏季赛team数据.csv', index=False)
lpl2020summerplayerSet.to_csv('LPL2020夏季赛player数据.csv', index=False)
lpl2020summerheroSet.to_csv('LPL2020夏季赛hero数据.csv', index=False)
lpl2021springteamSet.to_csv('LPL2021春季赛team数据.csv', index=False)
lpl2021springplayerSet.to_csv('LPL2021春季赛player数据.csv', index=False)
lpl2021springheroSet.to_csv('LPL2021春季赛hero数据.csv', index=False)
lpl2021summerteamSet.to_csv('LPL2021夏季赛team数据.csv', index=False)
lpl2021summerplayerSet.to_csv('LPL2021夏季赛player数据.csv', index=False)
lpl2021summerheroSet.to_csv('LPL2021夏季赛hero数据.csv', index=False)
lpl2022springteamSet.to_csv('LPL2022春季赛team数据.csv', index=False)
lpl2022springplayerSet.to_csv('LPL2022春季赛player数据.csv', index=False)
lpl2022springheroSet.to_csv('LPL2022春季赛hero数据.csv', index=False)

end = time.perf_counter()  # 记录数据获取与预处理结束时间
print('LPL2020Spring~2022Spring数据清洗、写入已完成！共计耗时{:.3f}秒'.format(end - start))