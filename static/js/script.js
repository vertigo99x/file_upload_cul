
const checkMode = () => {
    if(localStorage.getItem('mode')==='dark'){
        document.querySelector('body').classList.add('dark-mode-variables')
    } else if(localStorage.getItem('mode')===null){
        localStorage.setItem('mode','light')
        document.querySelector('body').classList.remove('dark-mode-variables')
    }
}


const changeMode = () => {
    if (localStorage.getItem('mode') === 'light'){
        localStorage.setItem('mode','dark')
        document.querySelector('body').classList.add('dark-mode-variables')
    } else {
        localStorage.setItem('mode','light')
        document.querySelector('body').classList.remove('dark-mode-variables')
    }
}


checkMode()


//======================================================




//===========================================================
var itemArr = []
var checkBoxValue = false
const selectAllMeals = (arr) => {
    if(checkBoxValue === false){
        for(let x = 1; x < arr.length+1; arr++){
            document.querySelector(`#checkbox${x}`).checked=true
            checkBoxValue = true;
            itemArr.push(arr[x-1])
        }
    } else {
        for(let x = 1; x < arr.length+1; arr++){
            document.querySelector(`#checkbox${x}`).checked=false;
            checkBoxValue = false;
        }
        itemArr = []
    }
}

const manageItemArr = (item) => {
    const index = itemArr.indexOf(item);
    if(index != -1){
        itemArr.splice(index,1)
        document.querySelector(`#checkbox${item}`).checked=false;
    } else {
        itemArr.push(item)
        document.querySelector(`#checkbox${item}`).checked=true;
    }
    if(itemArr.length == 0){
        document.querySelector('#selectAll').checked=false;
    }
}



const recipeData = (meals, summary) => {
      
    var ingredients = meals.ingredients
    var steps = meals.instructions
    
    box = document.querySelector('#recipeBox')

    box.innerHTML = '';
    box.innerHTML += `
        <form style="overflow-y:scroll;max-height:40em;position:relative;">
        <div class="modal-header d-flex" style='flex-direction:column;'>
        <p><span class="material-icons" style="color:var(--warning);">timer</span> ${ meals.cookTime } Mins </p>
        <h4 class="modal-title">${ meals.mealName }</h4>
        
        </div>
        <div class="modal-body">
        <div class="form-group" style="position:relative;text-align:center">
            <img style="width:100%;height:12em;border-radius:.8em;box-shadow:var(--box-shadow);" src="${ meals.image }" />
        </div>
        
        <div class="form-group" style="text-align:left">
            <p style="font-size:12px;">
              ${ summary }
            </p>
            
        </div>
        <div class="form-group" style="text-align:left">
            
            <p style="text-align:center;font-weight:bold;">Ingredients for ${ meals.servings } servings</p>
            <div class="" style="display:flex; flex-direction:column;" id="ingredientsList">
                
            </div>
        </div>

        <div class="form-group" style="position:relative;text-align:left;margin:0 0 8em 0">
            <p style="text-align:center;font-weight:bold;">Steps:</p>
            <table class="table table-hover table striped">
            <thead>
                <tr>
                  <td><p>Steps</p></td>
                  <td><p>Procedure</p></td>
                </tr>
            </thead>
            <tbody id="stepsBody">

            </tbody>
            </table>
        </div>
        
        </div>
        <div class="modal-footer" style="position:fixed;bottom:0;width:100%">
        <input type="button" class="btn btn-danger" data-dismiss="modal"  value="Cancel">
        
        </div>
    </form>
    `

    var ingredientsList = document.getElementById('ingredientsList')
    var stepsBody = document.getElementById('stepsBody')

    for(let x = 0; x < ingredients.length; x++){
      var ingredient = ingredients[x]
      ingredientsList.innerHTML += `
        <div><a href="${ingredient.image}" style="color:var(--img-link);font-size:15px;">${ingredient.name}</a></div>            
      `
    }

    for(let x = 0; x < steps.length; x++){
      var step = steps[x];
      stepsBody.innerHTML += `
          <tr>
            <td><p>${ step.no }</p></td>
            <td><p>${ step.procedure }</p></td>
          </tr>

      `
    }

}