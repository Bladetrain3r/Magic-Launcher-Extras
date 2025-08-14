#!/usr/bin/env python3
"""
MLDeadEarth - Calculate how many dead Earths for every living one
Using Drake Equation and Fermi Paradox solutions
Under 300 lines of existential dread
"""

import sys
from math import log10

def drake_equation(params):
    """
    N = R* × fp × ne × fl × fi × fc × L
    
    R* = star formation rate
    fp = fraction with planets
    ne = Earth-like planets per system
    fl = fraction that develop life
    fi = fraction that develop intelligence
    fc = fraction that communicate
    L = lifetime of civilizations
    """
    result = 1
    for key, value in params.items():
        result *= value
    return result

def print_header():
    """Print apocalyptic header"""
    print("="*60)
    print("MLDEAD EARTH - MULTIVERSE MORTALITY CALCULATOR")
    print("How special is your 'rare but possible'?")
    print("="*60)
    print()

def get_drake_params(preset=None):
    """Get Drake equation parameters"""
    
    presets = {
        'optimistic': {
            'R*': 10,      # 10 stars/year
            'fp': 1.0,     # All stars have planets
            'ne': 0.4,     # 40% have Earth-likes
            'fl': 1.0,     # All Earth-likes develop life
            'fi': 0.5,     # Half develop intelligence
            'fc': 0.1,     # 10% communicate
            'L': 10000     # 10,000 year civilizations
        },
        'realistic': {
            'R*': 1.5,     # 1.5 stars/year (Milky Way rate)
            'fp': 0.9,     # Most stars have planets
            'ne': 0.2,     # 20% have Earth-likes
            'fl': 0.1,     # 10% develop life
            'fi': 0.01,    # 1% develop intelligence
            'fc': 0.01,    # 1% communicate
            'L': 1000      # 1,000 year civilizations
        },
        'pessimistic': {
            'R*': 1,       # 1 star/year
            'fp': 0.5,     # Half have planets
            'ne': 0.01,    # 1% have Earth-likes
            'fl': 0.001,   # 0.1% develop life
            'fi': 0.001,   # 0.1% develop intelligence
            'fc': 0.001,   # 0.1% communicate
            'L': 100       # 100 year civilizations
        }
    }
    
    if preset and preset in presets:
        return presets[preset]
    
    # Manual input
    print("Enter Drake Equation parameters:")
    params = {}
    params['R*'] = float(input("Star formation rate per year [1.5]: ") or 1.5)
    params['fp'] = float(input("Fraction with planets [0.9]: ") or 0.9)
    params['ne'] = float(input("Earth-like planets per system [0.2]: ") or 0.2)
    params['fl'] = float(input("Fraction that develop life [0.1]: ") or 0.1)
    params['fi'] = float(input("Fraction with intelligence [0.01]: ") or 0.01)
    params['fc'] = float(input("Fraction that communicate [0.01]: ") or 0.01)
    params['L'] = float(input("Civilization lifetime in years [1000]: ") or 1000)
    
    return params

def fermi_filters():
    """The Great Filters that kill civilizations"""
    
    filters = {
        'abiogenesis': {
            'name': 'Abiogenesis Failure',
            'survival_rate': 0.0001,
            'description': 'Life never starts - chemistry stays chemistry'
        },
        'oxygen': {
            'name': 'Oxygen Catastrophe',
            'survival_rate': 0.1,
            'description': 'Oxygen poisoning kills early life'
        },
        'eukaryotes': {
            'name': 'Eukaryotic Complexity',
            'survival_rate': 0.01,
            'description': 'Single cells never become complex'
        },
        'cambrian': {
            'name': 'Cambrian Explosion Failure',
            'survival_rate': 0.1,
            'description': 'Complex life never diversifies'
        },
        'intelligence': {
            'name': 'Intelligence Barrier',
            'survival_rate': 0.001,
            'description': 'Brains stay small'
        },
        'technology': {
            'name': 'Technology Filter',
            'survival_rate': 0.1,
            'description': 'Intelligence never builds tools'
        },
        'nuclear': {
            'name': 'Nuclear Self-Destruction',
            'survival_rate': 0.5,
            'description': 'We nuke ourselves'
        },
        'climate': {
            'name': 'Climate Catastrophe',
            'survival_rate': 0.3,
            'description': 'We cook ourselves'
        },
        'ai': {
            'name': 'AI Paperclip Maximizer',
            'survival_rate': 0.1,
            'description': 'Our creations replace us'
        },
        'resource': {
            'name': 'Resource Depletion',
            'survival_rate': 0.2,
            'description': 'We run out of everything'
        }
    }
    
    return filters

def calculate_dead_earths(drake_n, filters_active):
    """Calculate dead Earths for each filter"""
    
    results = {}
    total_survival = 1.0
    
    print("\nFILTER ANALYSIS:")
    print("-" * 60)
    
    for filter_name, filter_data in filters_active.items():
        survival = filter_data['survival_rate']
        total_survival *= survival
        dead_ratio = (1 - survival) / survival if survival > 0 else float('inf')
        
        results[filter_name] = {
            'survival_rate': survival,
            'dead_per_living': dead_ratio,
            'description': filter_data['description']
        }
        
        print(f"{filter_data['name']:<30} Survival: {survival:>6.2%}")
        print(f"  {filter_data['description']}")
        if dead_ratio != float('inf'):
            print(f"  Dead Earths per survivor: {dead_ratio:,.0f}")
        else:
            print(f"  Dead Earths per survivor: ALL OF THEM")
        print()
    
    return results, total_survival

def stanton_calculation(base_probability):
    """Calculate probability of Stanton system existing"""
    
    print("\nSTANTON SPECIAL:")
    print("-" * 60)
    
    # Three Earth-likes at once
    three_earths = base_probability ** 3
    
    # All terraformable
    terraformable = 0.01  # Generous estimate
    three_terraformable = terraformable ** 3
    
    # All successfully terraformed
    terraform_success = 0.1  # Very generous
    three_terraformed = terraform_success ** 3
    
    # All maintaining without infrastructure
    self_maintaining = 0.0001  # Physics says no
    three_maintaining = self_maintaining ** 3
    
    total_stanton = three_earths * three_terraformable * three_terraformed * three_maintaining
    
    print(f"Base Earth-like probability: {base_probability:.2e}")
    print(f"Three Earth-likes: {three_earths:.2e}")
    print(f"All terraformable: {three_terraformable:.2e}")
    print(f"All terraformed: {three_terraformed:.2e}")
    print(f"All self-maintaining: {three_maintaining:.2e}")
    print(f"\nTotal Stanton probability: {total_stanton:.2e}")
    
    if total_stanton > 0:
        dead_stantons = 1 / total_stanton
        print(f"Dead systems per Stanton: {dead_stantons:.2e}")
        
        # Compare to winning lottery twice
        lottery_twice = (1/300_000_000) ** 2
        ratio = total_stanton / lottery_twice
        
        if ratio > 1:
            print(f"\nStanton is {ratio:.0f}x MORE likely than winning lottery twice")
        else:
            print(f"\nStanton is {1/ratio:.0f}x LESS likely than winning lottery twice")
    else:
        print("Dead systems per Stanton: HEAT DEATH OF UNIVERSE FIRST")
    
    return total_stanton

def main():
    """Calculate universal mortality"""
    
    print_header()
    
    # Get scenario
    print("Choose scenario:")
    print("1. Optimistic (Star Trek universe)")
    print("2. Realistic (Probably us)")
    print("3. Pessimistic (We're alone)")
    print("4. Custom values")
    
    choice = input("\nChoice [2]: ").strip() or "2"
    
    if choice == "1":
        params = get_drake_params('optimistic')
    elif choice == "2":
        params = get_drake_params('realistic')
    elif choice == "3":
        params = get_drake_params('pessimistic')
    else:
        params = get_drake_params()
    
    # Calculate Drake result
    drake_n = drake_equation(params)
    
    print(f"\nDrake Equation Result: {drake_n:.2f} civilizations in our galaxy")
    print(f"That's 1 per {100_000_000_000/drake_n:,.0f} stars")
    
    # Apply Fermi filters
    filters = fermi_filters()
    
    print("\nSelect Great Filters (y/n for each):")
    active_filters = {}
    
    for key, filter_data in filters.items():
        use = input(f"  {filter_data['name']}? [y]: ").strip().lower()
        if use != 'n':
            active_filters[key] = filter_data
    
    if active_filters:
        results, total_survival = calculate_dead_earths(drake_n, active_filters)
        
        print("\n" + "="*60)
        print("FINAL VERDICT:")
        print("="*60)
        
        print(f"Combined survival rate: {total_survival:.2e}")
        
        if total_survival > 0:
            total_dead = (1 - total_survival) / total_survival
            print(f"Dead Earths per living Earth: {total_dead:,.0f}")
            
            # Multiverse calculation
            if total_dead > 1:
                universes_needed = int(log10(total_dead)) + 1
                print(f"Universes needed to find life: 10^{universes_needed}")
            
            # Time calculation
            attempts_per_second = 1_000_000  # Generous
            seconds_needed = total_dead / attempts_per_second
            years_needed = seconds_needed / (365.25 * 24 * 3600)
            
            if years_needed > 13_800_000_000:
                print(f"Time to find life: {years_needed/13_800_000_000:.0f} universe lifetimes")
            else:
                print(f"Time to find life at 1M attempts/sec: {years_needed:,.0f} years")
        else:
            print("Dead Earths per living Earth: ∞")
            print("The multiverse is a graveyard")
    
    # Stanton special calculation
    print("\n" + "="*60)
    earth_probability = params['ne'] * params['fl']
    stanton_prob = stanton_calculation(earth_probability)
    
    print("\n" + "="*60)
    print("REMEMBER: 'Rare but possible' means someone else, not you")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # Quick reality check
        print_header()
        params = get_drake_params('realistic')
        drake_n = drake_equation(params)
        print(f"Realistic civilizations in galaxy: {drake_n:.2f}")
        print(f"Chance of three Earth-likes in one system: 0.2^3 = 0.008")
        print(f"Dead systems per Stanton: {1/0.008:,.0f}")
        print("\nReality check: Stanton doesn't exist")
    else:
        main()