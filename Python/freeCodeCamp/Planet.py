class Planet:
    def __init__(self, name, planet_type, star):
        if any(not isinstance(arg, str) for arg in (name, planet_type, star)) :
            raise TypeError('name, planet type, and star must be strings')
        if any(not arg for arg in (name, planet_type, star)):
            raise ValueError('name, planet_type, and star must be non-empty strings')
        self.name = name
        self.planet_type = planet_type
        self.star = star
    
    def orbit(self):
        return f"{self.name} is orbiting around {self.star}..."
    
    def __str__(self):
        return f"Planet: {self.name} | Type: {self.planet_type} | Star: {self.star}"