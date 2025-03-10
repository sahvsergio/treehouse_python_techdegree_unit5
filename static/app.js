
let navigation = document.querySelector(".navigation"); 

function addNavigation(projects) {
  let navBar=document.createElement('nav');
  let containerFluid=document.createElement('div');
  navigation.insert
 
}
  
 

  
/*

<nav class="navbar navbar-expand-lg">
                <div class="container-fluid">
                  <a class="navbar-brand" href="#">Sergio Herrera</a>
                  <button class="toggle" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                  </button>
                  <div class="collapse navbar-collapse" id="navbarContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                      <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="{{url_for('index')}}">Home</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="{{url_for('about')}}">About</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="{{url_for('index')+'#skills'}}">Skills</a>
                      </li>
                      <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                          Projects
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                          {% for  project in projects %}
                            <li><a class="dropdown-item" href="{{url_for('detail', id=project.id)}}">{{ project.title }}</a></li>
                          {% endfor %}
                          
                        </ul>
                      
                      <li class="nav-item">
                        <a class="nav-link" href="{{url_for('index')+'#contact'}}">Contact</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="{{url_for('create')}}">Add Project</a>
                      </li>
                    </ul>
                  </div>
                </div>
            </nav>

*/