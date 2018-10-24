<template>
    <div id='app' onload="document.body.scrollTop = document.body.scrollHeight">
        <topNav>Demo</topNav>
        <div class='main'>
        <bubble v-for="msg in messages" v-bind:location="msg.loation">{{msg.text}}</bubble>
        </div>
        <input-panel></input-panel>
    </div>
</template>

<script>
import bubble from './components/bubble'
import topNav from './components/nav'
import inputPanel from './components/input'

export default {
name: 'app',
components: {
    bubble,
    topNav,
    inputPanel,
},
data () {
    return {
    messages: [
        {
        loation: 'left',
        text: '欢迎使用天气查询机器人Demo'
        }
    ],
    uid: 1
    }
},
mounted: function() {
    var that = this
    this.bus.$on('send', function(data){ //data: input内容
    console.log('get send')
    console.log(that.messages)
    that.messages.push({
        loation: 'right',
        text: data
    })
    document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight;
    })
    this.bus.$on('getRes', function(res){
    console.log(res)
    try{
        that.messages.push({
        loation: 'left',
        text: res.data.res.text
        })
    } catch(e) {
        that.messages.push({
        loation: 'left',
        text: '服务发生异常'
        })
    }
    
    })
}

}
</script>

<style>
#app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}
.main {
    position: relative;
    top: 3rem;
}

::-webkit-scrollbar{ /*不显示滚动条*/
    display: none;
}
</style>
