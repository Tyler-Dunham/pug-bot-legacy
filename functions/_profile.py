class ProfileMixin:# Mixin allows us to separate our methods from queue_commands.py. 
                   # We are simply adding these functions to the QueueCommands class but storing them in this file.

    def check_valid_elo(self, elos: list):
        new_elos = []

        # Check if elo is in range
        for elo in elos:
            if (elo) not in range(0, 5001):          
                return None
            # Finalize elos in new_elos (Default elos if 0)
            elo = elo if elo != 0 else 2500
            new_elos.append(elo)
        
        return new_elos