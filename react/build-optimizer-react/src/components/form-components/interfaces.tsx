export interface Weapon{
    name: string,
    somber: boolean,
    affinity: string,
    pngUrl: string,
    isPow:boolean
}
export interface Armor{
    name:string,
    weight:number,
    poise:number,
    pngUrl: string
}
export interface Talisman{
    name:string,
    pngUrl:string,
    effect:string
}
export interface Spell{
    name:string,
    pngUrl:string,
    type:string,
    effect:string,
    cost:number,
    slots:number
}