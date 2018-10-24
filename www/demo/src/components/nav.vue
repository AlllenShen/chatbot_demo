<template>
    <div id='top-nav'>
        <div class="title"><slot></slot></div>    
    </div>
</template>

<script>
export default {
    name: 'top-nav'
}
</script>

<style scoped>
    #top-nav {
        border-bottom: 1px solid #DFDFDF;
        position: fixed;
        top: 0;
        z-index: 100;
        width: 100%;
        font-size: 1.2rem;
        height: 3rem;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
    }
</style>

 