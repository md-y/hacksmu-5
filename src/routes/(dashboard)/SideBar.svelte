<script>

</script>

<div id="sidebar">
    <h1>Our Project Name</h1>
    <!-- Links here -->
    <div class="sidebarItem">
        <a href="/">Dashboard</a>
    </div>
    <div class="sidebarItem">
        <a href="account">Account</a>
    </div>
    {#each {length: 5} as _ , i}
        <div class="sidebarItem">
            <a href="#/">Link {i + 2} </a>
        </div>
    {/each}
</div>

<style>
    a{
        color: white;
        text-decoration: none;
    }
    a:hover{
        color: white;
        text-decoration: none;
    }
    h1{
        color: white;
        text-align: center;
    }
    #sidebar{
        display:flex;
        flex-direction: column;
        background-color: #4e73df;
        background-image: linear-gradient(180deg,#4e73df 10%,#224abe 100%);
        background-size: cover;
        width: 14rem!important; 
        height: 100vh;
    }
    .sidebarItem{
        height: 25px;
        color:white;
        margin-left: 20px;
        width: 14rem!important; 
    }
</style>