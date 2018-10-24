<template>
<div>
    <Row class="input-panel">
        <Col span='3'>
            <Icon type="ios-mic" size='32'/>
        </Col>
        <Col span='18'>
            <Input v-model="value" class="my-input" type="text" placeholder="输入您的问题"/>
        </Col>
        <Col span='3'>
            <Icon @click="send()" type="ios-arrow-forward" size='32'/>
        </Col>
    </Row>
</div>
</template>


<script>

export default {
    name: 'input-panel',
    data () {
        return {
            value: "",
            url: 'http://127.0.0.1:8888/api/weather_chat'
        }
    },
    methods: {
        send: function() {
            // console.log(this.value);
            if (this.value === '')
                return
            this.bus.$emit('send', this.value)
            this.$http.jsonp(
                this.url,
                { 
                    params: {
                        uid: 1, 
                        message: { 
                            text: this.value
                        } 
                    }, 
                    headers: {
                        contentType: 'application/json'
                    } 
                },
            ).then(res => {
                this.bus.$emit('getRes', res)
            })
            this.value = ''
        },
    }
}
</script>

<style scoped>
.input-panel {
    border-top: 1px solid #DFDFDF;
    position: fixed;
    bottom: 0;
    width: 100%;
    min-height: 3rem;
    max-height: 3rem;  
    align-items: center;
    flex-wrap: nowrap;
    display: flex;
    background-color: white;
}
.holder {
    width: 100%;
    border-radius: 2rem;
    border: 2rpx solid #DFDFDF;
}

.my-input:hover, .my-input:focus {
    box-shadow: 0;
    border: 2rpx solid #DFDFDF;
}


</style>

