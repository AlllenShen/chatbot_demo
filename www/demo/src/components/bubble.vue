<template>
    <div class='bubble' :class="location">
        <div class='innder-text'>
            <div class="inner-text"><slot></slot></div> 
        </div>
    </div>
</template>

<script>
export default {
    name: 'bubble',
    props: {
        location: String,
    },
}
</script>

<style>
.bubble {
    position: relative;
    border-radius: 0.5rem;
    max-width: 55%;
    width: fit-content;
    display: flex;
    justify-content:center;
    align-items:center;
    margin-top: 1rem;
    min-height: 2rem;
    color: white;
}

.left {
    float: left;
    background-color: #404b69;
    margin-left: 0.8rem;
    clear: both;
}

.right {
    float: right;
    clear: both;
    background-color: #00818a;
    margin-right: 0.8rem;
}

.innder-text {
    font-size: 1rem;
    margin: 0.5rem 0.5rem 0.5rem 0.5rem;
    text-align: left
}
</style>
