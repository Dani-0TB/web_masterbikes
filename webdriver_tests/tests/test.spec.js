const { Builder, By, Key } = require('selenium-webdriver');
const { Options } = require('selenium-webdriver/chrome');
let options = new Options();
let driver = undefined;

beforeAll(async () => {
  options.windowSize({width:1500,height:800})
  driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build()
  await driver.manage().setTimeouts({implicit: 5000});
});

afterAll(async () =>{
  await driver.quit();
});

describe('Pruebas previas:', () => {
  test('Selenium abre la pagina principal', async () => {
    await driver.get('http://localhost:8000');
    let title = await driver.getTitle();
    expect(title).toBe("Inicio");
  });
  
  test('Navegar al login', async ()=>{
    let login = await driver.findElement(By.linkText("Login"));
    await login.click();
    expect(await driver.getCurrentUrl())
    .toBe("http://localhost:8000/accounts/login/")
  });
})

describe('Pruebas de login',() => {

  let usuarios = [
    {name:'admin',pass:'Testing321'},
    {name:'admin',pass:'Testing'},
    {name:'admin',pass:''},
    {name:'',pass:'Testing321'},
    {name:'fasdfdas',pass:'3213sadsa'}
  ];
  
  let userIndex = 0;
  let usuario = undefined;

  beforeEach( async () =>{
    usuario = usuarios[userIndex];
    await driver.get('http://localhost:8000/accounts/login/');
    await driver.findElement(By.id('id_username')).sendKeys(usuario.name);
    await driver.findElement(By.id('id_password')).sendKeys(usuario.pass);
    await driver.actions()
      .keyDown(Key.ENTER)
      .keyUp(Key.ENTER)
      .perform();
  })

  afterEach(async () => {
    userIndex += 1;
    usuario = undefined
  });

  test('Login con usuario existente', async () => {
    let userCheck = await driver.findElement(By.css('.dropdown-toggle')).getText()
    expect(userCheck).toBe("admin");
  });

  test('Login con usuario existente y contraseña incorrecta', async () => {
    let alert = await driver.findElement(By.css('.text-warning')).getText()
    expect(alert).toMatch("Error al validar el formulario:");
  });

  test('Login con usuario existente y sin contraseña', async () => {
    let errorList = await driver.findElement(By.css('.errorlist')).getText()
    expect(errorList).toMatch("Este campo es obligatorio");
  });

  test('Login sin usuario y con contraseña', async () => {
    let errorList = await driver.findElement(By.css('.errorlist')).getText()
    expect(errorList).toMatch("Este campo es obligatorio");
  });

  test('Login con datos al azar', async () => {
    let alert = await driver.findElement(By.css('.text-warning')).getText()
    expect(alert).toMatch("Error al validar el formulario:");
  });
});


