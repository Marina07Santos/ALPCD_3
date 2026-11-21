# ALPCD_3
grupo: Leonor, Luísa, Marina
| Leonor Costa  | A113681 |
| Luísa Meneses | A113976 |
| Marina Santos | A114844 |


A  FitCli utilizou em python as seguintes bibliotecas `typer` e `requests` para consultar exercícios da API pública **wger** (`https://wger.de/api/v2/`).


## Organização dos ficheiros
| Ficheiro | Conteúdo |
|----------|----------|
| main.py | Lógica: pedidos à API, cache, filtros, classificação e contagens |
| fitcli.py | Interface: comandos do typer, validação dos argumentos e saída em JSON/CSV |
| requirements.txt | Bibliotecas externas (requests, typer) |
| partes_individuais/ | Versões de cada elemento do grupo antes de juntarmos tudo no main.py (o programa não as usa) |


## Instalação
pip install -r requirements.txt



## Exemplos do top
python fitcli.py top 10            
[
  {
    "name": "Single-Arm Backpack Row",
    "category": "Back",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "Lateral Bound to Stick",
    "category": "Legs",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "Standing Broad Jump",
    "category": "Legs",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "Approach Jump",
    "category": "Legs",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "Countermovement Jump (CMJ)",
    "category": "Legs",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "Pogo jumps",
    "category": "Calves",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "TRX/Rings Dip",
    "category": "Chest",
    "equipment": []
  },
  {
    "name": "TRX/Rings Face Pull",
    "category": "Shoulders",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "TRX/Rings Y Raise",
    "category": "Shoulders",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  },
  {
    "name": "TRX/Rings Push-Up",
    "category": "Chest",
    "equipment": [
      "none (bodyweight exercise)"
    ]
  }
]



## Exemplos do search
### 1
python fitcli.py search biceps 5
[
  {
    "name": "Biceps Curls With Barbell",
    "category": "Arms",
    "equipment": [
      "Barbell"
    ]
  },
  {
    "name": "Biceps Curls With Dumbbell",
    "category": "Arms",
    "equipment": [
      "Dumbbell"
    ]
  },
  {
    "name": "Biceps Curls With SZ-bar",
    "category": "Arms",
    "equipment": [
      "SZ-Bar"
    ]
  },
  {
    "name": "Biceps Curl With Cable",
    "category": "Arms",
    "equipment": [
      "Cable machine"
    ]
  },
  {
    "name": "Chin Up",
    "category": "Back",
    "equipment": [
      "Pull-up bar"
    ]
  }
]


### 2
python fitcli.py search legs 2  
[
  {
    "name": "Seated Hip Adduction",
    "category": "Legs",
    "equipment": []
  },
  {
    "name": "Barbell Hack Squats",
    "category": "Legs",
    "equipment": [
      "Barbell"
    ]
  }
]


### 3
python fitcli.py search "abs back" 3
[
  {
    "name": "2 Handed Kettlebell Swing",
    "category": "Abs",
    "equipment": [
      "Kettlebell"
    ]
  },
  {
    "name": "Barbell Ab Rollout",
    "category": "Abs",
    "equipment": [
      "Barbell"
    ]
  },
  {
    "name": "Abdominal Stabilization",
    "category": "Abs",
    "equipment": [
      "Gym mat"
    ]
  }
]


### 4
python fitcli.py search bicep 2        
[
  {
    "name": "Biceps Curls With Barbell",
    "category": "Arms",
    "equipment": [
      "Barbell"
    ]
  },
  {
    "name": "Biceps Curls With Dumbbell",
    "category": "Arms",
    "equipment": [
      "Dumbbell"
    ]
  }
]



## Exemplos do type
### 1
python fitcli.py type 999
compound


### 2
python fitcli.py type 688
isolated


### 3
python fitcli.py type 2761
other


### 4
python fitcli.py type 2480
cardio



## Exemplos do equipment
### 1
python fitcli.py equipment chest  
[
  {
    "bench": 37
  },
  {
    "dumbbell": 25
  },
  {
    "cable": 20
  },
  {
    "machine": 12
  },
  {
    "bodyweight": 3
  },
  {
    "incline bench": 1
  },
  {
    "barbell": 1
  }
]


### 2
python fitcli.py equipment abs    
[
  {
    "dumbbell": 11
  },
  {
    "bench": 9
  },
  {
    "barbell": 7
  },
  {
    "mat": 7
  },
  {
    "cable": 6
  },
  {
    "kettlebell": 5
  },
  {
    "machine": 4
  },
  {
    "band": 4
  },
  {
    "pull-up": 4
  },
  {
    "bodyweight": 2
  }
]



## Exemplos do workout
### 1
python fitcli.py workout biceps,back compound 5
{
  "biceps": [
    {
      "name": "Chin Up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Hercules Pillars",
      "type": "compound",
      "equipment": [
        "Cable machine"
      ]
    },
    {
      "name": "Muscle up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Wall Slides",
      "type": "compound",
      "equipment": [
        "none (bodyweight exercise)"
      ]
    },
    {
      "name": "Pullup on fingerboard",
      "type": "compound",
      "equipment": [
        "none (bodyweight exercise)"
      ]
    }
  ],
  "back": [
    {
      "name": "Bent Over Dumbbell Rows (Single Arm)",
      "type": "compound",
      "equipment": [
        "Bench",
        "Dumbbell"
      ]
    },
    {
      "name": "Bent Over Rowing",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Bent Over Rowing Reverse",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Chin Up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Close-grip Lat Pull Down",
      "type": "compound",
      "equipment": []
    }
  ]
}


### 2
python fitcli.py workout biceps,back compound 5
{
  "biceps": [
    {
      "name": "Chin Up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Hercules Pillars",
      "type": "compound",
      "equipment": [
        "Cable machine"
      ]
    },
    {
      "name": "Muscle up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Wall Slides",
      "type": "compound",
      "equipment": [
        "none (bodyweight exercise)"
      ]
    },
    {
      "name": "Pullup on fingerboard",
      "type": "compound",
      "equipment": [
        "none (bodyweight exercise)"
      ]
    }
  ],
  "back": [
    {
      "name": "Bent Over Dumbbell Rows (Single Arm)",
      "type": "compound",
      "equipment": [
        "Bench",
        "Dumbbell"
      ]
    },
    {
      "name": "Bent Over Rowing",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Bent Over Rowing Reverse",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Chin Up",
      "type": "compound",
      "equipment": [
        "Pull-up bar"
      ]
    },
    {
      "name": "Close-grip Lat Pull Down",
      "type": "compound",
      "equipment": []
    }
  ]
}


### 3
python fitcli.py workout biceps isolated 3     
{
  "biceps": [
    {
      "name": "Biceps Curls With Barbell",
      "type": "isolated",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Biceps Curls With Dumbbell",
      "type": "isolated",
      "equipment": [
        "Dumbbell"
      ]
    },
    {
      "name": "Biceps Curls With SZ-bar",
      "type": "isolated",
      "equipment": [
        "SZ-Bar"
      ]
    }
  ]
}


### 4
python fitcli.py workout abs,legs any 3   
{
  "abs": [
    {
      "name": "2 Handed Kettlebell Swing",
      "type": "compound",
      "equipment": [
        "Kettlebell"
      ]
    },
    {
      "name": "Barbell Ab Rollout",
      "type": "isolated",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Abdominal Stabilization",
      "type": "compound",
      "equipment": [
        "Gym mat"
      ]
    }
  ],
  "legs": [
    {
      "name": "Seated Hip Adduction",
      "type": "isolated",
      "equipment": []
    },
    {
      "name": "Barbell Hack Squats",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Barbell Lunges Standing",
      "type": "compound",
      "equipment": [
        "Barbell"
      ]
    }
  ]
}


### 5
python fitcli.py workout bicep,xpto any 2
Sem exercicios para: xpto
{
  "bicep": [
    {
      "name": "Biceps Curls With Barbell",
      "type": "isolated",
      "equipment": [
        "Barbell"
      ]
    },
    {
      "name": "Biceps Curls With Dumbbell",
      "type": "isolated",
      "equipment": [
        "Dumbbell"
      ]
    }
  ],
  "xpto": []
}


### 6
python fitcli.py workout chest,shoulders isolated 3 --csv treino.csv
Ficheiro exportado: treino.csv (6 registos)