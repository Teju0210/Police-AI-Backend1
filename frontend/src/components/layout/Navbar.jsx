import {
  Bell,
  Search,
  UserCircle,
  Moon,
  Sun,
  X,
} from "lucide-react";

import { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Navbar() {

  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const [isLightMode, setIsLightMode] = useState(false);

  const toggleLightMode = () => {
    if (isLightMode) {
      document.documentElement.classList.remove("light-mode");
    } else {
      document.documentElement.classList.add("light-mode");
    }
    setIsLightMode(!isLightMode);
  };


  const officerName =
    localStorage.getItem("officerName") || "Praveen";



  const handleLogout = () => {

    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("officerName");

    navigate("/");

  };



  const searchItems = [
    "FIR Reports",
    "Crime Heatmap",
    "Criminal Network",
    "Active Cases",
    "Suspects",
    "AI Analysis",
    "Crime Analytics",
  ];



  const filteredResults = searchItems.filter((item)=>
    item.toLowerCase()
    .includes(search.toLowerCase())
  );



  const date = new Date().toLocaleDateString(
    "en-IN",
    {
      day:"numeric",
      month:"short",
      year:"numeric"
    }
  );



  return (

<header
className="
h-20
px-8
flex
items-center
justify-between
bg-[#111827]/70
backdrop-blur-xl
border-b
border-white/10
"
>



{/* SEARCH */}

<div className="relative w-full max-w-md">


<div
className="
flex
items-center
bg-white/5
border
border-white/10
rounded-xl
px-4
"
>


<Search
size={20}
className="text-slate-400"
/>


<input

value={search}

onChange={(e)=>{
setSearch(e.target.value);
setShowSearch(true);
}}

onFocus={()=>{
setShowSearch(true);
}}

placeholder="Search FIR, Crime, Suspect..."

className="
w-full
bg-transparent
outline-none
text-white
placeholder:text-slate-400
px-3
py-3
"

/>



{
search &&

<X

size={18}

className="
cursor-pointer
text-slate-400
"

onClick={()=>{
setSearch("");
setShowSearch(false);
}}

/>

}


</div>




{/* SEARCH RESULTS */}

{

showSearch && search && (

<div
className="
absolute
top-14
left-0
w-full
bg-[#111827]
border
border-white/10
rounded-xl
shadow-xl
z-50
overflow-hidden
"
>


{

filteredResults.length > 0 ?

filteredResults.map((item)=>(

<div

key={item}

onClick={()=>{

setSearch(item);
setShowSearch(false);

}}

className="
px-4
py-3
text-slate-300
hover:bg-blue-500/20
cursor-pointer
transition
"

>

{item}

</div>

))

:

<p
className="
p-4
text-slate-400
"
>
No results found
</p>

}


</div>

)

}


</div>






{/* RIGHT SIDE */}


<div
className="
flex
items-center
gap-5
"
>



{/* DATE */}

<div
className="
hidden
lg:block
text-right
"
>

<p
className="
text-sm
text-slate-300
"
>

{date}

</p>


<p
className="
text-xs
text-green-400
"
>

● System Online

</p>


</div>







{/* DARK MODE */}
<button
  onClick={toggleLightMode}
  className="
    p-3
    rounded-xl
    bg-white/5
    border
    border-white/10
    hover:bg-blue-500/20
    transition
  "
>
  {isLightMode ? <Sun size={22}/> : <Moon size={22}/>}
</button>







{/* NOTIFICATION */}

<button

className="
relative
p-3
rounded-xl
bg-white/5
border
border-white/10
hover:bg-blue-500/20
transition
"

>

<Bell size={22}/>


<span
className="
absolute
top-2
right-2
h-2.5
w-2.5
rounded-full
bg-red-500
animate-pulse
"
/>


</button>








{/* PROFILE */}

<div

className="
flex
items-center
gap-3
px-4
py-2
rounded-xl
bg-white/5
border
border-white/10
"

>


<UserCircle

size={40}

className="
text-cyan-400
"

/>



<div>

<p
className="
font-semibold
text-white
"
>

{officerName}

</p>


<p
className="
text-xs
text-slate-400
"
>

Karnataka Police

</p>


</div>


</div>







{/* LOGOUT */}

<button

onClick={handleLogout}

className="
px-5
py-2
rounded-xl
bg-red-500/20
text-red-400
border
border-red-500/30
hover:bg-red-500/30
transition
"

>

Logout

</button>



</div>



</header>

  );

}
