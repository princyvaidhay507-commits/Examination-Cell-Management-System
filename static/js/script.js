// ===============================
// Show / Hide Password
// ===============================

function togglePassword() {

    let password = document.getElementById("password");

    if (!password) return;

    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}


// ===============================
// Live Search Student
// ===============================

function searchStudent() {

    let input = document.getElementById("searchInput");

    if (!input) return;

    let filter = input.value.toUpperCase();

    let table = document.getElementById("studentTable");

    if (!table) return;

    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td")[1];

        if (td) {

            let txtValue = td.textContent || td.innerText;

            if (txtValue.toUpperCase().indexOf(filter) > -1) {

                tr[i].style.display = "";

            } else {

                tr[i].style.display = "none";
            }
        }
    }
}


// ===============================
// Delete Confirmation
// ===============================

function confirmDelete() {

    return confirm("Are you sure you want to delete this student?");
}


// ===============================
// Dark Mode
// ===============================

function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

    } else {

        localStorage.setItem("theme", "light");
    }

}


window.onload = function () {

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");
    }

};


// ===============================
// Loader
// ===============================

window.addEventListener("load", function () {

    let loader = document.querySelector(".loader");

    if (loader) {

        loader.style.display = "none";
    }

});


// ===============================
// Sidebar Active Link
// ===============================

let links = document.querySelectorAll(".sidebar a");

links.forEach(function(link){

    link.addEventListener("click",function(){

        links.forEach(function(item){
            item.classList.remove("active");
        });

        this.classList.add("active");

    });

});


// ===============================
// Dashboard Welcome
// ===============================

console.log("Examination Cell Management System Loaded Successfully");


// ===============================
// Table Row Hover
// ===============================

let rows = document.querySelectorAll("tbody tr");

rows.forEach(function(row){

    row.addEventListener("mouseenter",function(){

        this.style.transition="0.3s";

    });

});


// ===============================
// Current Date
// ===============================

let date = document.getElementById("currentDate");

if(date){

    let today = new Date();

    date.innerHTML = today.toDateString();

}


// ===============================
// Auto Close Alert
// ===============================

setTimeout(function(){

    let alert = document.querySelector(".alert");

    if(alert){

        alert.style.display="none";

    }

},3000);


// ===============================
// Smooth Scroll
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href")).scrollIntoView({

            behavior:"smooth"

        });

    });

});


// ===============================
// Dashboard Counter Animation
// ===============================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    counter.innerText = "0";

    const updateCounter = () => {

        const target = +counter.getAttribute("data-target");

        const count = +counter.innerText;

        const increment = target / 50;

        if(count < target){

            counter.innerText = `${Math.ceil(count + increment)}`;

            setTimeout(updateCounter,20);

        }else{

            counter.innerText = target;

        }

    };

    updateCounter();

});