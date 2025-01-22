import pygame

NEIGHBOUR_OFFSETS = [(-1, 0), (-1, -1), (0,-1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # tuple list
PHYSICS_TILES = {'grass', 'stone'} # set (no duplicates allowed) faster than list

class Tilemap:
    def __init__(self, game, tile_size=16): 
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(13): # 0-25
            self.tilemap[str(6 + i) + ';8'] = {'type': 'grass', 'variant': 1, 'pos': (6 + i, 8)} # 10 long horizontal line of grass tiles starting from 3
            self.tilemap[str(6 + i) + ';9'] = {'type': 'grass', 'variant': 7, 'pos': (6 + i, 9)} # 10 long horizontal line of grass tiles starting from 3
            
            # ^ will become 3;10 and 10;3strings
    def tiles_around(self, pos): #have to convert pixel pos. to grid
        nearbyTiles=[]
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # // = integer division
        for offset in NEIGHBOUR_OFFSETS: # goes over each tuple in offsets, and assigns offset with them one at a time
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                nearbyTiles.append(self.tilemap[check_loc]) # appends which tile was touched
        return nearbyTiles # returns which tiles are near
    
    def physics_rects_around(self, pos): # only some tiles have colission, we get pos from entities
        rects = []
        for tile in self.tiles_around(pos): # looks at each 
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) # all four corners of the square in x and y??
        return rects
                
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos']) # render them first, background stuff

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size)) # [][] because in the dictionary we only gave grass and not the variant

    def offsets_around(self, pos): #have to convert pixel pos. to grid
        nearbyTiles=[]
        
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # // = integer division
        for offset in NEIGHBOUR_OFFSETS: # goes over each tuple in offsets, and assigns offset with them one at a time
            
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                nearbyTiles.append(NEIGHBOUR_OFFSETS[self.i]) # appends which tile was touched
                self.i +=1
        self.i = 0
        return nearbyTiles # returns which tiles are near
