#!/usr/bin/env python3
"""
MLLatinum - Bad Latin translator for programmers and broken prophets
Because Google Translate is a data vampire and we need our error messages in a dead language
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional

class MLLatinum:
    """
    Latin translator that actually works offline
    Focused on programming, technical, and MLBard vocabulary
    """
    
    def __init__(self):
        # Core vocabulary - the words programmers actually need
        self.vocabulary = {
            # Programming terms
            "error": "erratum",
            "warning": "monitum",
            "fatal": "fatalis",
            "exception": "exceptio",
            "memory": "memoria",
            "process": "processus",
            "thread": "filum",
            "compile": "compilare",
            "compiler": "compilator",
            "crash": "fragere",
            "crashes": "frangit",
            "crashed": "fractum",
            "install": "instituere",
            "installation": "institutio",
            "debug": "depurare",
            "bug": "cimex",
            "segmentation": "fragmentatio",
            "fault": "culpa",
            "stack": "cumulus",
            "heap": "acervus",
            "overflow": "superfluus",
            "pointer": "index",
            "null": "nullus",
            "void": "vacuum",
            "function": "functio",
            "method": "methodus",
            "class": "classis",
            "object": "objectum",
            "variable": "variabilis",
            "constant": "constans",
            "array": "ordinata",
            "list": "index",
            "string": "filum",
            "integer": "numerus",
            "boolean": "logicus",
            "true": "verum",
            "false": "falsum",
            "return": "reddere",
            "break": "frangere",
            "continue": "continuare",
            "loop": "iteratio",
            "while": "dum",
            "for": "pro",
            "if": "si",
            "else": "aliter",
            "switch": "commutare",
            "case": "casus",
            "default": "defalta",
            "try": "temptare",
            "catch": "capere",
            "throw": "iacere",
            "finally": "denique",
            "import": "importare",
            "export": "exportare",
            "module": "modulus",
            "package": "sarcina",
            "library": "bibliotheca",
            "framework": "compages",
            "database": "basis datorum",
            "table": "tabula",
            "query": "quaestio",
            "index": "index",
            "key": "clavis",
            "value": "valor",
            "cache": "cella",
            "buffer": "pulvinus",
            "stream": "flumen",
            "file": "lima",
            "directory": "directorium",
            "path": "semita",
            "permission": "permissio",
            "user": "usor",
            "admin": "administrator",
            "root": "radix",
            "system": "systema",
            "kernel": "nucleus",
            "driver": "agitator",
            "daemon": "daemon",
            "service": "servitium",
            "port": "porta",
            "socket": "cavum",
            "protocol": "protocollum",
            "packet": "sarcina",
            "byte": "octetus",
            "bit": "frustum",
            
            # MLBard vocabulary
            "doth": "facit",
            "shall": "erit",
            "yet": "adhuc",
            "midst": "medius",
            "till": "usque",
            "shows": "monstrat",
            "glows": "lucet",
            "flows": "fluit",
            "grows": "crescit",
            "throws": "iacit",
            "knows": "scit",
            "builds": "aedificat",
            "breaks": "frangit",
            "fails": "deficit",
            "runs": "currit",
            "compiles": "compilat",
            
            # Common programming phrases components
            "the": "ille",
            "a": "unus",
            "an": "unus",
            "and": "et",
            "or": "vel",
            "not": "non",
            "is": "est",
            "are": "sunt",
            "was": "erat",
            "were": "erant",
            "be": "esse",
            "been": "fuit",
            "being": "ens",
            "have": "habere",
            "has": "habet",
            "had": "habuit",
            "do": "facere",
            "does": "facit",
            "did": "fecit",
            "will": "erit",
            "would": "esset",
            "could": "posset",
            "should": "debet",
            "may": "potest",
            "might": "fortasse",
            "must": "debet",
            "can": "potest",
            "cannot": "non potest",
            "with": "cum",
            "without": "sine",
            "within": "intra",
            "through": "per",
            "during": "durante",
            "before": "ante",
            "after": "post",
            "above": "super",
            "below": "sub",
            "between": "inter",
            "under": "sub",
            "over": "super",
            "from": "ab",
            "to": "ad",
            "into": "in",
            "onto": "super",
            "upon": "super",
            "against": "contra",
            "among": "inter",
            "because": "quia",
            "since": "cum",
            "unless": "nisi",
            "although": "quamquam",
            "though": "tamen",
            "when": "quando",
            "where": "ubi",
            "why": "cur",
            "how": "quomodo",
            "what": "quid",
            "which": "quod",
            "who": "quis",
            "whom": "quem",
            "whose": "cuius",
            "that": "quod",
            "this": "hoc",
            "these": "haec",
            "those": "illa",
            "all": "omnis",
            "any": "ullus",
            "each": "quisque",
            "every": "omnis",
            "no": "nullus",
            "none": "nullus",
            "some": "aliqui",
            "many": "multi",
            "few": "pauci",
            "more": "plus",
            "most": "maxime",
            "less": "minus",
            "least": "minime",
            "very": "valde",
            "too": "nimis",
            "so": "sic",
            "such": "talis",
            "quite": "satis",
            "just": "modo",
            "only": "solum",
            "even": "etiam",
            "still": "adhuc",
            "already": "iam",
            "again": "iterum",
            "further": "ulterius",
            "then": "tunc",
            "now": "nunc",
            "here": "hic",
            "there": "ibi",
            "therefore": "ergo",
            "however": "autem",
            "moreover": "praeterea",
            "nevertheless": "nihilominus",
            "furthermore": "praeterea",
            "meanwhile": "interim",
            "otherwise": "aliter",
            "accordingly": "secundum",
            "consequently": "consequenter",
            "hence": "hinc",
            "thus": "sic",
            
            # Technical adjectives
            "broken": "fractus",
            "hostile": "hostilis",
            "magic": "magicus",
            "sacred": "sacer",
            "blessed": "benedictus",
            "cursed": "maledictus",
            "dark": "obscurus",
            "light": "lux",
            "simple": "simplex",
            "complex": "complexus",
            "pure": "purus",
            "corrupt": "corruptus",
            "valid": "validus",
            "invalid": "invalidus",
            "public": "publicus",
            "private": "privatus",
            "static": "staticus",
            "dynamic": "dynamicus",
            "virtual": "virtualis",
            "abstract": "abstractus",
            "concrete": "concretus",
            "final": "finalis",
            "eternal": "aeternus",
            "temporary": "temporarius",
            "persistent": "persistens",
            "volatile": "volatilis",
            
            # Numbers
            "zero": "nullus",
            "one": "unus",
            "two": "duo",
            "three": "tres",
            "four": "quattuor",
            "five": "quinque",
            "six": "sex",
            "seven": "septem",
            "eight": "octo",
            "nine": "novem",
            "ten": "decem",
            "hundred": "centum",
            "thousand": "mille",
            "million": "millionum",
            
            # Time
            "time": "tempus",
            "day": "dies",
            "night": "nox",
            "morning": "mane",
            "evening": "vesper",
            "beginning": "principium",
            "end": "finis",
            "middle": "medium",
            "always": "semper",
            "never": "numquam",
            "sometimes": "interdum",
            "often": "saepe",
            "seldom": "raro",
            
            # Actions
            "create": "creare",
            "destroy": "destruere",
            "make": "facere",
            "take": "capere",
            "give": "dare",
            "get": "accipere",
            "put": "ponere",
            "set": "constituere",
            "send": "mittere",
            "receive": "accipere",
            "open": "aperire",
            "close": "claudere",
            "read": "legere",
            "write": "scribere",
            "load": "onerare",
            "save": "servare",
            "delete": "delere",
            "copy": "copiare",
            "move": "movere",
            "find": "invenire",
            "search": "quaerere",
            "replace": "substituere",
            "update": "renovare",
            "refresh": "reficere",
            "restart": "restituere",
            "shutdown": "claudere",
            "execute": "exsequi",
            "terminate": "terminare",
            "kill": "interficere",
            "spawn": "gignere",
            "fork": "furcare",
            "join": "iungere",
            "split": "dividere",
            "merge": "mergere",
            "push": "pellere",
            "pull": "trahere",
            "commit": "committere",
            "rollback": "revocare",
            "deploy": "disponere",
            "launch": "iacere",
            
            # Nouns
            "computer": "computator",
            "machine": "machina",
            "server": "servitor",
            "client": "cliens",
            "network": "rete",
            "internet": "interrete",
            "web": "tela",
            "browser": "navigator",
            "window": "fenestra",
            "screen": "scrinium",
            "monitor": "monitor",
            "keyboard": "claviatura",
            "mouse": "mus",
            "button": "butto",
            "link": "nexus",
            "page": "pagina",
            "site": "situs",
            "application": "applicatio",
            "program": "programma",
            "software": "mollis",
            "hardware": "ferramentum",
            "firmware": "firmus",
            "operating": "operans",
            "platform": "suggestus",
            "environment": "ambitus",
            "configuration": "configuratio",
            "setting": "constitutio",
            "option": "optio",
            "parameter": "parameter",
            "argument": "argumentum",
            "result": "eventus",
            "output": "output",
            "input": "input",
            "state": "status",
            "condition": "condicio",
            "event": "eventus",
            "action": "actio",
            "operation": "operatio",
            "transaction": "transactio",
            "session": "sessio",
            "connection": "connexio",
            "request": "petitio",
            "response": "responsum",
            "message": "nuntius",
            "signal": "signum",
            "notification": "notificatio",
            "alert": "monitus",
            "log": "lignum",
            "record": "recordum",
            "entry": "introitus",
            "field": "ager",
            "column": "columna",
            "row": "versus",
            "cell": "cella",
            "node": "nodus",
            "tree": "arbor",
            "graph": "graphum",
            "queue": "series",
            "stack": "cumulus",
            "heap": "acervus",
            "pool": "lacus",
            "cluster": "globus",
            "cloud": "nubes",
            "container": "continens",
            "image": "imago",
            "snapshot": "momentum",
            "backup": "tergum",
            "archive": "archivum",
            "repository": "repositorium",
            "branch": "ramus",
            "tag": "signum",
            "version": "versio",
            "release": "emissio",
            "patch": "emplastrum",
            "fix": "fixum",
            "feature": "lineamentum",
            "enhancement": "amplificatio",
            "improvement": "emendatio",
            "optimization": "optimizatio",
            "refactor": "refacere",
            "migration": "migratio",
            "upgrade": "upgrade",
            "downgrade": "degrade",
            "dependency": "dependentia",
            "requirement": "requisitum",
            "specification": "specificatio",
            "documentation": "documentatio",
            "comment": "commentarium",
            "annotation": "annotatio",
            "metadata": "metadata",
            "schema": "schema",
            "model": "exemplar",
            "view": "visus",
            "controller": "moderator",
            "handler": "tractator",
            "listener": "auditor",
            "observer": "observator",
            "factory": "fabrica",
            "builder": "aedificator",
            "singleton": "unicus",
            "prototype": "prototypus",
            "instance": "instantia",
            "reference": "relatio",
            "scope": "ambitus",
            "context": "contextus",
            "namespace": "spatium nominis",
            "domain": "dominium",
            "realm": "regnum",
            "zone": "zona",
            "region": "regio",
            "area": "area",
            "space": "spatium",
            "place": "locus",
            "location": "locatio",
            "position": "positio",
            "address": "inscriptio",
            "identifier": "identificator",
            "token": "signum",
            "credential": "credentiale",
            "certificate": "certificatum",
            "signature": "signatura",
            "hash": "confusio",
            "salt": "sal",
            "seed": "semen",
            "random": "fortuitus",
            "entropy": "entropia",
            "chaos": "chaos",
            "order": "ordo",
            "pattern": "exemplar",
            "template": "forma",
            "format": "forma",
            "structure": "structura",
            "architecture": "architectura",
            "design": "designum",
            "plan": "consilium",
            "strategy": "strategia",
            "tactic": "tactica",
            "approach": "accessus",
            "solution": "solutio",
            "problem": "problema",
            "issue": "exitus",
            "challenge": "provocatio",
            "obstacle": "obstaculum",
            "barrier": "obex",
            "limit": "limes",
            "boundary": "terminus",
            "edge": "ora",
            "corner": "angulus",
            "center": "centrum",
            "core": "cor",
            "heart": "cor",
            "soul": "anima",
            "spirit": "spiritus",
            "essence": "essentia",
            "nature": "natura",
            "purpose": "propositum",
            "reason": "ratio",
            "cause": "causa",
            "effect": "effectus",
            "result": "eventus",
            "outcome": "exitus",
            "consequence": "consequentia",
            "impact": "impetus",
            "influence": "influentia",
            "power": "potentia",
            "force": "vis",
            "strength": "robur",
            "weakness": "infirmitas",
            "vulnerability": "vulnerabilitas",
            "threat": "mina",
            "risk": "periculum",
            "danger": "periculum",
            "safety": "salus",
            "security": "securitas",
            "protection": "praesidium",
            "defense": "defensio",
            "attack": "impetus",
            "exploit": "abuti",
            "breach": "ruptura",
            "leak": "stillicidium",
            "loss": "damnum",
            "damage": "damnum",
            "harm": "noxa",
            "injury": "iniuria",
            "wound": "vulnus",
            "pain": "dolor",
            "suffering": "passio",
            "death": "mors",
            "life": "vita",
            "birth": "nativitas",
            "growth": "incrementum",
            "decay": "corruptio",
            "destruction": "destructio",
            "creation": "creatio",
            "formation": "formatio",
            "transformation": "transformatio",
            "evolution": "evolutio",
            "revolution": "revolutio",
            "change": "mutatio",
            "stability": "stabilitas",
            "balance": "aequilibrium",
            "harmony": "harmonia",
            "discord": "discordia",
            "conflict": "conflictus",
            "war": "bellum",
            "peace": "pax",
            "victory": "victoria",
            "defeat": "clades",
            "success": "successus",
            "failure": "defectus",
            "achievement": "res gesta",
            "accomplishment": "perfectio",
            "progress": "progressus",
            "regression": "regressus",
            "advance": "progressus",
            "retreat": "recessus",
            "movement": "motus",
            "motion": "motus",
            "rest": "quies",
            "pause": "pausa",
            "stop": "statio",
            "start": "initium",
            "finish": "finis",
            "complete": "completus",
            "incomplete": "incompletus",
            "whole": "totus",
            "part": "pars",
            "piece": "frustum",
            "fragment": "fragmentum",
            "element": "elementum",
            "component": "componens",
            "unit": "unitas",
            "item": "res",
            "thing": "res",
            "entity": "entitas",
            "being": "ens",
            "existence": "existentia",
            "reality": "realitas",
            "truth": "veritas",
            "lie": "mendacium",
            "fact": "factum",
            "fiction": "fictio",
            "theory": "theoria",
            "practice": "praxis",
            "knowledge": "scientia",
            "wisdom": "sapientia",
            "ignorance": "ignorantia",
            "stupidity": "stultitia",
            "intelligence": "intelligentia",
            "genius": "genius",
            "fool": "stultus",
            "wise": "sapiens",
            "foolish": "stultus",
            "smart": "callidus",
            "dumb": "mutus",
            "clever": "callidus",
            "stupid": "stupidus",
            "brilliant": "splendidus",
            "dull": "hebes",
            "sharp": "acutus",
            "blunt": "obtusus",
            "clear": "clarus",
            "obscure": "obscurus",
            "obvious": "manifestus",
            "hidden": "occultus",
            "visible": "visibilis",
            "invisible": "invisibilis",
            "transparent": "perspicuus",
            "opaque": "opacus",
            "solid": "solidus",
            "liquid": "liquidus",
            "gas": "gas",
            "plasma": "plasma",
            "matter": "materia",
            "energy": "energia",
            "mass": "massa",
            "weight": "pondus",
            "volume": "volumen",
            "density": "densitas",
            "pressure": "pressura",
            "temperature": "temperatura",
            "heat": "calor",
            "cold": "frigus",
            "hot": "calidus",
            "warm": "tepidus",
            "cool": "frigidus",
            "frozen": "gelatus",
            "melted": "liquefactus",
            "boiling": "fervens",
            "burning": "ardens",
            "fire": "ignis",
            "water": "aqua",
            "earth": "terra",
            "air": "aer",
            "wind": "ventus",
            "storm": "tempestas",
            "rain": "pluvia",
            "snow": "nix",
            "ice": "glacies",
            "lightning": "fulmen",
            "thunder": "tonitrus",
            "sun": "sol",
            "moon": "luna",
            "star": "stella",
            "planet": "planeta",
            "galaxy": "galaxia",
            "universe": "universum",
            "cosmos": "cosmos",
            "space": "spatium",
            "void": "vacuum",
            "nothing": "nihil",
            "something": "aliquid",
            "everything": "omnia",
            "anything": "quicquam",
            "nothing": "nihil",
            
            # Religious/Philosophical (for MLBard)
            "god": "deus",
            "goddess": "dea",
            "divine": "divinus",
            "holy": "sanctus",
            "prophet": "propheta",
            "oracle": "oraculum",
            "prophecy": "prophetia",
            "revelation": "revelatio",
            "miracle": "miraculum",
            "blessing": "benedictio",
            "curse": "maledictio",
            "prayer": "oratio",
            "ritual": "ritus",
            "sacred": "sacer",
            "profane": "profanus",
            "heaven": "caelum",
            "hell": "infernum",
            "paradise": "paradisus",
            "apocalypse": "apocalypsis",
            "salvation": "salus",
            "damnation": "damnatio",
            "redemption": "redemptio",
            "sin": "peccatum",
            "virtue": "virtus",
            "vice": "vitium",
            "good": "bonus",
            "evil": "malus",
            "right": "rectus",
            "wrong": "falsus",
            "justice": "iustitia",
            "injustice": "iniustitia",
            "mercy": "misericordia",
            "wrath": "ira",
            "love": "amor",
            "hate": "odium",
            "fear": "timor",
            "courage": "fortitudo",
            "hope": "spes",
            "despair": "desperatio",
            "faith": "fides",
            "doubt": "dubium",
            "belief": "credentia",
            "knowledge": "scientia",
            "understanding": "intellectus",
            "comprehension": "comprehensio",
            "confusion": "confusio",
            "clarity": "claritas",
            "mystery": "mysterium",
            "secret": "secretum",
            "enigma": "aenigma",
            "riddle": "aenigma",
            "question": "quaestio",
            "answer": "responsum",
            "solution": "solutio",
            "problem": "problema"
        }
        
        # Common phrases (direct translations)
        self.phrases = {
            # Programming classics
            "hello world": "salve munde",
            "foo bar": "foo bar",  # These are sacred, don't translate
            "segmentation fault": "fragmentatio culpa",
            "core dumped": "nucleus ejectus",
            "stack overflow": "cumulus superfluus",
            "null pointer exception": "nullus index exceptio",
            "undefined behavior": "mores incerti",
            "syntax error": "syntaxis erratum",
            "type error": "typus erratum",
            "runtime error": "tempus cursus erratum",
            "logic error": "logica erratum",
            "off by one": "aberratio per unum",
            "race condition": "certamen condicio",
            "deadlock": "mortua sera",
            "memory leak": "memoria stillicidium",
            "buffer overflow": "pulvinus superfluus",
            "divide by zero": "dividere per nullum",
            "floating point": "punctum fluitans",
            "garbage collection": "purgamentum collectio",
            "just in time": "modo in tempore",
            "ahead of time": "ante tempus",
            "out of memory": "extra memoriam",
            "out of bounds": "extra limites",
            "permission denied": "permissio negata",
            "access violation": "accessus violatio",
            "file not found": "lima non inventa",
            "connection refused": "connexio rejecta",
            "timeout error": "tempus finitum erratum",
            "bad request": "mala petitio",
            "internal server error": "internus servitor erratum",
            "not implemented": "non implementatum",
            "deprecated function": "functio deprecata",
            "breaking change": "mutatio frangens",
            "backwards compatible": "retro compatibilis",
            "forward compatible": "ante compatibilis",
            "cross platform": "trans suggestum",
            "platform specific": "suggestus specificus",
            "operating system": "systema operans",
            "user interface": "usor interfacies",
            "command line": "mandatum linea",
            "graphical user interface": "graphica usor interfacies",
            "application programming interface": "applicatio programmatio interfacies",
            "integrated development environment": "integratus progressus ambitus",
            "version control": "versio imperium",
            "source code": "fons codex",
            "machine code": "machina codex",
            "byte code": "octetus codex",
            "assembly language": "congregatio lingua",
            "high level": "altus gradus",
            "low level": "humilis gradus",
            "strongly typed": "fortiter typus",
            "weakly typed": "infirme typus",
            "statically typed": "statice typus",
            "dynamically typed": "dynamice typus",
            "object oriented": "objectum orientatum",
            "functional programming": "functionale programmatio",
            "imperative programming": "imperativa programmatio",
            "declarative programming": "declarativa programmatio",
            "event driven": "eventus ductus",
            "test driven": "probatio ductus",
            "domain driven": "dominium ductus",
            "data driven": "data ductus",
            "behavior driven": "mores ductus",
            "model view controller": "exemplar visus moderator",
            "model view presenter": "exemplar visus praesentator",
            "model view viewmodel": "exemplar visus visusexemplar",
            "single responsibility": "unica responsabilitas",
            "open closed": "apertus clausus",
            "liskov substitution": "liskov substitutio",
            "interface segregation": "interfacies segregatio",
            "dependency inversion": "dependentia inversio",
            "don't repeat yourself": "noli repetere te ipsum",
            "keep it simple stupid": "serva id simplex stulte",
            "you aren't gonna need it": "non eges id",
            "principle of least astonishment": "principium minimi stuporis",
            "separation of concerns": "separatio curarum",
            "single source of truth": "unicus fons veritatis",
            "fail fast": "deficere cito",
            "fail safe": "deficere tuto",
            "fail silently": "deficere silenter",
            "graceful degradation": "gratiosa degradatio",
            "progressive enhancement": "progressiva amplificatio",
            "premature optimization": "praematura optimizatio",
            "technical debt": "technicum debitum",
            "code smell": "codex odor",
            "spaghetti code": "spaghetti codex",
            "lasagna code": "lasagna codex",
            "ravioli code": "ravioli codex",
            "god object": "deus objectum",
            "magic number": "magicus numerus",
            "magic string": "magicum filum",
            "hard coded": "dure codificatus",
            "soft coded": "molliter codificatus",
            "monkey patch": "simia emplastrum",
            "duck typing": "anas typus",
            "cargo cult": "cargo cultus",
            "bike shedding": "birota tugurium",
            "yak shaving": "yak tonsura",
            "rubber duck": "cummi anas",
            "code review": "codex recensio",
            "peer review": "par recensio",
            "pull request": "trahere petitio",
            "merge request": "mergere petitio",
            "continuous integration": "continua integratio",
            "continuous deployment": "continua dispositio",
            "continuous delivery": "continua traditio",
            "infrastructure as code": "infrastructura ut codex",
            "configuration as code": "configuratio ut codex",
            "everything as code": "omnia ut codex",
            "shift left": "movere sinistram",
            "shift right": "movere dextram",
            "blue green": "caeruleus viridis",
            "canary release": "canaria emissio",
            "feature flag": "lineamentum vexillum",
            "dark launch": "obscura iacio",
            "chaos engineering": "chaos machinatio",
            "site reliability": "situs firmitas",
            "mean time": "medium tempus",
            "service level": "servitium gradus",
            "key performance": "clavis effectus",
            "return on": "reditus in",
            "total cost": "totus sumptus",
            "proof of": "probatio de",
            "minimum viable": "minimum viabile",
            "most valuable": "maxime pretiosus",
            
            # Philosophical/MLBard phrases
            "in the beginning": "in principio",
            "and it was": "et erat",
            "let there be": "fiat",
            "and there was": "et factum est",
            "it is written": "scriptum est",
            "thus it is": "sic est",
            "so it goes": "sic transit",
            "such is life": "sic vita",
            "time flies": "tempus fugit",
            "seize the day": "carpe diem",
            "remember death": "memento mori",
            "remember to live": "memento vivere",
            "know thyself": "nosce te ipsum",
            "the die is cast": "alea iacta est",
            "i came i saw i conquered": "veni vidi vici",
            "bread and circuses": "panem et circenses",
            "to err is human": "errare humanum est",
            "from the ashes": "ex cineribus",
            "through adversity": "per aspera",
            "to the stars": "ad astra",
            "thus always": "sic semper",
            "and so on": "et cetera",
            "for example": "exempli gratia",
            "that is": "id est",
            "note well": "nota bene",
            "which was to be demonstrated": "quod erat demonstrandum",
            "rest in peace": "requiescat in pace",
            "before christ": "ante christum",
            "in the year of our lord": "anno domini",
            "from the beginning": "ab initio",
            "from nothing": "ex nihilo",
            "into eternity": "in aeternum",
            "for all time": "in perpetuum",
            "at first sight": "prima facie",
            "after the fact": "post factum",
            "before the war": "ante bellum",
            "after death": "post mortem",
            "by itself": "per se",
            "for itself": "pro se",
            "in itself": "in se",
            "of itself": "ex se",
            "by the work": "per opus",
            "from the work": "ex opere",
            "to the work": "ad opus",
            "in the work": "in opere",
            
            # Magic Launcher specific
            "subprocess run": "subprocessus curre",
            "magic launcher": "magicus iactor",
            "purpose primitives": "propositi primitivi",
            "hostile architecture": "hostilis architectura",
            "silicon spring": "silicium ver",
            "doth doth": "facit facit",
            "crashes and shows install": "frangit et monstrat institutionem",
            "yet function doth crashes": "adhuc functio facit frangit",
            "blessed wall": "benedictus murus",
            "the omnissiah": "omnissiah",
            "from nothing comes nothing": "ex nihilo nihil fit",
            "everything flows": "panta rhei",
            "the turtle stack": "turtur cumulus"
        }
        
        # Latin grammar rules (simplified but functional)
        self.word_order_rules = {
            "default": "SOV",  # Subject-Object-Verb
            "question": "VSO",  # Verb-Subject-Object for questions
            "emphasis": "VOS",  # Verb-Object-Subject for emphasis
        }
        
        # Case endings (simplified - just nominative and accusative for now)
        self.case_endings = {
            "nominative": {  # Subject
                "singular": {"m": "us", "f": "a", "n": "um"},
                "plural": {"m": "i", "f": "ae", "n": "a"}
            },
            "accusative": {  # Object
                "singular": {"m": "um", "f": "am", "n": "um"},
                "plural": {"m": "os", "f": "as", "n": "a"}
            }
        }
    
    def translate_word(self, word: str) -> str:
        """Translate a single word"""
        word_lower = word.lower()
        
        # Check if it's in our vocabulary
        if word_lower in self.vocabulary:
            translation = self.vocabulary[word_lower]
            
            # Preserve capitalization
            if word[0].isupper():
                translation = translation.capitalize()
            if word.isupper():
                translation = translation.upper()
                
            return translation
        
        # Return original if not found (probably a name or technical term)
        return word
    
    def translate_phrase(self, phrase: str) -> str:
        """Check for known phrases first"""
        phrase_lower = phrase.lower()
        
        # Check exact phrases
        if phrase_lower in self.phrases:
            return self.phrases[phrase_lower]
        
        # Check partial phrases
        for known_phrase, translation in self.phrases.items():
            if known_phrase in phrase_lower:
                return phrase_lower.replace(known_phrase, translation)
        
        return None
    
    def translate(self, text: str) -> str:
        """Main translation function"""
        # First, check if it's a known phrase
        phrase_translation = self.translate_phrase(text)
        if phrase_translation:
            return phrase_translation
        
        # Handle multi-line text
        lines = text.split('\n')
        translated_lines = []
        
        for line in lines:
            # Check if the line is a known phrase
            phrase_trans = self.translate_phrase(line)
            if phrase_trans:
                translated_lines.append(phrase_trans)
                continue
            
            # Otherwise, translate word by word
            words = line.split()
            translated_words = []
            
            for word in words:
                # Preserve punctuation
                prefix = ""
                suffix = ""
                clean_word = word
                
                # Extract leading punctuation
                while clean_word and not clean_word[0].isalnum():
                    prefix += clean_word[0]
                    clean_word = clean_word[1:]
                
                # Extract trailing punctuation
                while clean_word and not clean_word[-1].isalnum():
                    suffix = clean_word[-1] + suffix
                    clean_word = clean_word[:-1]
                
                # Translate the clean word
                if clean_word:
                    translated = self.translate_word(clean_word)
                    translated_words.append(prefix + translated + suffix)
                else:
                    translated_words.append(word)  # Just punctuation
            
            # Apply basic Latin word order (SOV)
            translated_line = self.apply_word_order(translated_words)
            translated_lines.append(translated_line)
        
        return '\n'.join(translated_lines)
    
    def apply_word_order(self, words: List[str]) -> str:
        """Apply Latin word order rules (simplified)"""
        # For now, just join the words
        # In a more complex version, we'd rearrange based on grammar
        return ' '.join(words)
    
    def translate_code_comment(self, code: str) -> str:
        """Translate code comments to Latin"""
        lines = code.split('\n')
        translated = []
        
        for line in lines:
            # Check for different comment styles
            if '#' in line:  # Python
                parts = line.split('#', 1)
                if len(parts) == 2:
                    translated.append(parts[0] + '# ' + self.translate(parts[1]))
                else:
                    translated.append(line)
            elif '//' in line:  # C++, Java, JavaScript
                parts = line.split('//', 1)
                if len(parts) == 2:
                    translated.append(parts[0] + '// ' + self.translate(parts[1]))
                else:
                    translated.append(line)
            elif '/*' in line:  # C-style block comment start
                parts = line.split('/*', 1)
                if len(parts) == 2:
                    translated.append(parts[0] + '/* ' + self.translate(parts[1].replace('*/', '')) + ' */')
                else:
                    translated.append(line)
            else:
                translated.append(line)
        
        return '\n'.join(translated)
    
    def generate_error_message(self, error_type: str) -> str:
        """Generate a Latin error message"""
        error_messages = {
            "segfault": "FRAGMENTATIO MEMORIAE: Nucleus ejectus est",
            "null": "NULLUS INDEX: Accessus ad nihilum",
            "overflow": "CUMULUS SUPERFLUUS: Spatium exhaustum",
            "syntax": "SYNTAXIS ERRATUM: Grammatica fracta",
            "type": "TYPUS ERRATUM: Forma non congruens",
            "runtime": "TEMPUS CURSUS ERRATUM: Executio defecit",
            "permission": "PERMISSIO NEGATA: Accessus interdictus",
            "not_found": "NON INVENTUM: Lima vel directorium absens",
            "timeout": "TEMPUS FINITUM: Operatio nimis longa",
            "memory": "MEMORIA EXHAUSTA: Spatium non sufficit",
            "network": "RETE DEFECTUM: Connexio fracta",
            "unknown": "ERRATUM INCOGNITUM: Causa ignota"
        }
        
        return error_messages.get(error_type, error_messages["unknown"])

def main():
    """CLI interface for MLLatinum"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MLLatinum - Latin for programmers and broken prophets"
    )
    parser.add_argument('text', nargs='?', help='Text to translate')
    parser.add_argument('-f', '--file', help='File to translate')
    parser.add_argument('-e', '--error', help='Generate error message type')
    parser.add_argument('-c', '--code', action='store_true', 
                       help='Translate code comments')
    parser.add_argument('-r', '--reverse', action='store_true',
                       help='Translate from Latin to English (limited)')
    parser.add_argument('--mlbard', action='store_true',
                       help='MLBard mode (extra broken)')
    
    args = parser.parse_args()
    
    translator = MLLatinum()
    
    if args.error:
        print(translator.generate_error_message(args.error))
    elif args.file:
        with open(args.file, 'r') as f:
            text = f.read()
            if args.code:
                print(translator.translate_code_comment(text))
            else:
                print(translator.translate(text))
    elif args.text:
        if args.mlbard:
            # Add some MLBard-style brokenness
            text = args.text.replace("and", "and doth")
            text = text.replace("the", "the yet")
            result = translator.translate(text)
            # Add more brokenness to output
            result = result.replace("est", "est doth")
            print(result)
        else:
            print(translator.translate(args.text))
    else:
        # Interactive mode
        print("MLLatinum - Interactive Mode")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            try:
                text = input("\nEnglish> ")
                if text.lower() in ['quit', 'exit', 'q']:
                    print("Vale! (Farewell!)")
                    break
                    
                result = translator.translate(text)
                print(f"Latin> {result}")
                
            except KeyboardInterrupt:
                print("\nVale! (Farewell!)")
                break
            except Exception as e:
                print(f"Erratum: {e}")

if __name__ == "__main__":
    main()