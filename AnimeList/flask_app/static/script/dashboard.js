// alert ('linked!')


const URL = 'https://kitsu.io/api/edge/anime?filter%5Btext%5D='
const resultDiv = document.querySelector('#animeResults')
const nameInput = document.querySelector('#query')

async function animeSearch(event) {
    event.preventDefault()
    console.log(nameInput.value)
    resultDiv.innerHTML = 'Loading....'
    let response = await fetch(URL + nameInput.value)
    let data = await response.json()
    console.log(data)
    resultDiv.innerHTML = `
                <div class="animeResults">
                <img src="${data.data[0].attributes.coverImage.tiny}" alt="${data.data[0].attributes.canonicalTitle}">
                <h4 class="mt-3">Anime Title: ${data.data[0].attributes.canonicalTitle}</h4>
                <p>Episodes: ${data.data[0].attributes.episodeCount}</p>
                <p>Status: ${data.data[0].attributes.status}</p>
                <p>Synopsis: ${data.data[0].attributes.description}</p>
                </div>
    `
}  


const picSpan = document.querySelector('#profilePic')

async function fetchPic() {
    let response = await fetch("https://api.waifu.pics/sfw/neko")
    let picData = await response.json()
    console.log(picData)
    picSpan.innerHTML = `
                <style>
                img {
                    border-radius: 50%;
                    width: 15rem;
                    height: 15rem;
                }
                </style>
                <img src="${picData.url}" alt="random_neko_pics">
                
    `
}

// fetchPic()

const recommendationsURL = 'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&sort=-favoritesCount,-popularityRank'
const recommendationDiv = document.querySelector('#recom_div')
const table = document.getElementById('table')

fetch(recommendationsURL)
.then( (response) => response.json())
.then( (data) => {
    data.data.forEach( (item) => {
        table.innerHTML += `
                <tr>
                    <td>${item.attributes.canonicalTitle}</td>
                    <td>${item.attributes.episodeCount}</td>
                    <td>${item.attributes.status}</td>
                </tr>
        `;
    })
})
.catch( (error) => console.log("Cannot get data"));

const randomQuotes = document.querySelector('#quotes')

async function fetchQuotes() {
    let response = await fetch('https://animechan.vercel.app/api/random')
    let quotesData = await response.json()
    randomQuotes.innerHTML = `
                    <p style="font-style: italic;">"${quotesData.quote}"</p>
                    <p>${quotesData.character} from ${quotesData.anime}</p>
    `
}

// fetchQuotes()