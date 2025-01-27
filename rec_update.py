import pygame
from receiver import Receiverobj
from tracker import Trackedobj


def init_receivers():
    """Initialize receivers with predefined positions."""
    return {
        "Rec1": Receiverobj("Rec1", 200, 200),
        "Rec2": Receiverobj("Rec2", 200, 400),
        "Rec3": Receiverobj("Rec3", 400, 200),
        "Rec4": Receiverobj("Rec4", 400, 400),
        "Rec5": Receiverobj("Rec5", 600, 200),
        "Rec6": Receiverobj("Rec6", 600, 400),
    }

def update_receivers(screen, receivers, tracked):
    for rec in receivers.values():
        rec.is_alive = True
    
    try:
        calculated_x, calculated_y, receivers_used = tracked.find_position(receivers)
    except ValueError as e:
        print(f"error: {e.args[0]}")
        return
    
    for rec in receivers.values():
        if not rec.is_alive:
            continue
        rec.is_active = False
        rec.is_primary = False
        rec.locate(tracked)
        if rec.name in receivers_used:
            rec.is_active = True
            pygame.draw.line(screen, "white", (calculated_x, calculated_y), (rec.x, rec.y), 1)
        if rec.name in receivers_used[0:2]:
            rec.is_primary = True
            pygame.draw.circle(screen, "white", (rec.x, rec.y), int(tracked.report(rec)), 1)
    return