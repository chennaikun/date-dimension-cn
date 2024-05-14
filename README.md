# chinese_holiday

#### 介绍
基于Fastapi实现的节假日查询接口API和日期维度数据API。

使用[holiday-cn](https://github.com/NateScarlet/holiday-cn)作为子项目.

#### 使用说明
 1. 克隆项目
 使用选项--recurse-submodules同时克隆holiday-cn项目
 ```bash
 git clone --recurse-submodules https://github.com/chennaikun/date-dimension-cn.git
 ```

 2. 如果要更新holiday-cn项目
 可以进入到oliday-cn目录中运行 git fetch 与 git merge，合并上游分支来更新本地代码。
 ```bash
 git fetch
 git merge origin/master
 ```

3. 运行
```bash
python main.py
```

4. docker运行
使用dockerfile构建镜像
```bash
docker build -t naikun/chinese_holiday .
```