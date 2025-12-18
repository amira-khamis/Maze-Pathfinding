import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque


# =========================
# Maze Logic
# =========================
class Maze:
    """Maze generation and management"""
    def __init__(self, width=20, height=12):
        self.width = width
        self.height = height
        self.start = (0, 0)
        self.goal = (width - 1, height - 1)
        self.grid = self._create_static_maze()

    def _create_static_maze(self):
        """Static maze - same every time"""
        grid = [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
        return grid

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x]==0

    def get_neighbors(self, x, y):
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        return [(x+dx, y+dy) for dx,dy in dirs if self.is_valid(x+dx, y+dy)]


# =========================
# Maze Visualization
# =========================
class MazeVisualizer:
    """Visualize maze with cartoon mouse and cheese"""
    settings = {
        'wall_color':"#313338",
        'wall_edge':'#1a202c',
        'wall_alpha':0.9,
        'cell_base':0.95,
        'cell_alpha':0.8,
        'mouse_color':'#8a8a8a',
        'mouse_ear':'#a8a8a8',
        'mouse_inner_ear':'#c8c8c8',
        'cheese_color':'#ffd700',
        'cheese_edge':'#daa520',
        'trail_color':'#4ecdc4'
    }

    def __init__(self, maze):
        self.maze = maze
        self.fig, self.ax = plt.subplots(figsize=(19,11))
        self.fig.patch.set_facecolor('#0a192f')
        self.ax.set_facecolor('#0a192f')
        self.mouse_artist = None
        self.path_line = None
        self.trail_dots = deque(maxlen=15)
        self.current_frame = 0

    def _draw_cell(self, x, y, is_wall):
        face = self.settings['wall_color'] if is_wall else plt.cm.Greys(self.settings['cell_base'] - (x+y*2)%4*0.02)
        edge = self.settings['wall_edge'] if is_wall else '#e2e8f0'
        hatch = '////' if is_wall else None
        alpha = self.settings['wall_alpha'] if is_wall else self.settings['cell_alpha']
        cell = patches.FancyBboxPatch((x,y),1,1, boxstyle="round,pad=0.02,rounding_size=0.1",
                                      facecolor=face, edgecolor=edge, linewidth=1.5, alpha=alpha, hatch=hatch)
        self.ax.add_patch(cell)
        if is_wall:
            self.ax.add_patch(patches.Circle((x+0.5,y+0.5),0.1,facecolor='#4a5568',alpha=0.3))

    def _draw_mouse(self, x, y, direction=(1,0)):
        if self.mouse_artist:
            for patch in self.mouse_artist: 
                patch.remove()
        cx, cy = x+0.5, y+0.5
        dx, dy = direction if direction!=(0,0) else (1,0)
        patches_list=[]
        patches_list.append(self.ax.add_patch(patches.Circle((cx,cy),0.3,facecolor=self.settings['mouse_color'],edgecolor='#6a6a6a',linewidth=1,zorder=20)))

        for ex in [-0.15,0.15]:
            patches_list.append(self.ax.add_patch(patches.Circle((cx+ex,cy-0.18),0.12,facecolor=self.settings['mouse_ear'],edgecolor='#888888',linewidth=0.5,zorder=21)))
            patches_list.append(self.ax.add_patch(patches.Circle((cx+ex,cy-0.18),0.072,facecolor=self.settings['mouse_inner_ear'],edgecolor='none',zorder=22)))

        patches_list.append(self.ax.add_patch(patches.Circle((cx-0.08,cy+0.05),0.06,facecolor='white',edgecolor='#aaaaaa',linewidth=0.5,zorder=23)))
        patches_list.append(self.ax.add_patch(patches.Circle((cx-0.05,cy+0.05),0.03,facecolor='black',zorder=24)))
        patches_list.append(self.ax.add_patch(patches.Circle((cx+0.08,cy+0.05),0.06,facecolor='white',edgecolor='#aaaaaa',linewidth=0.5,zorder=23)))
        patches_list.append(self.ax.add_patch(patches.Circle((cx+0.11,cy+0.05),0.03,facecolor='black',zorder=24)))

        patches_list.append(self.ax.add_patch(patches.Circle((cx,cy+0.15),0.03,facecolor='#444444',edgecolor='#333333',linewidth=0.3,zorder=25)))

        for side in [-1,1]:
            for i in [-1,0,1]:
                patches_list.append(self.ax.add_patch(patches.FancyArrow(cx+0.15*side,cy+0.1+i*0.04,0.2*side,0,width=0.005,facecolor='#888888',zorder=19)))

        patches_list.append(self.ax.add_patch(patches.Arc((cx,cy+0.2),0.15,0.08,theta1=200,theta2=340,color='#666666',linewidth=1,zorder=26)))
        self.mouse_artist=patches_list

    def _draw_cheese(self):
        x, y = self.maze.goal
        cx, cy = x+0.5, y+0.5
        triangle=[(cx+0.35,cy-0.25),(cx-0.35,cy),(cx+0.35,cy+0.25)]
        self.ax.add_patch(patches.Polygon(triangle,facecolor=self.settings['cheese_color'],edgecolor=self.settings['cheese_edge'],linewidth=1.5,zorder=5,joinstyle='round'))

        for i in range(5):
            dot_x = cx + (i-2)*0.08
            dot_y = cy + (i%2)*0.05 - 0.05
            dot_size = 0.015
            self.ax.add_patch(patches.Circle((dot_x,dot_y),dot_size,facecolor='#f4c542',alpha=0.7,edgecolor='none',zorder=6))

    def _draw_path_line(self,path,current_index):
        if len(path)>1:
            x_coords=[p[0]+0.5 for p in path[:current_index+1]]
            y_coords=[p[1]+0.5 for p in path[:current_index+1]]
            if self.path_line: 
                self.path_line.remove()
            self.path_line,=self.ax.plot(x_coords,y_coords,color='#ff6b6b',linewidth=3,alpha=0.8,zorder=4,
                                        marker='o',markersize=6,markerfacecolor='white',markeredgecolor='#ff6b6b',markeredgewidth=1.5)

    def _add_trail_dot(self,x,y,frame_number):
        dot_size = max(0.01,0.1-frame_number*0.002)
        dot_alpha = max(0.05,0.5-frame_number*0.01)
        trail_dot=patches.Circle((x+0.5,y+0.5),dot_size,facecolor=self.settings['trail_color'],alpha=dot_alpha,zorder=3)
        self.ax.add_patch(trail_dot)
        self.trail_dots.append(trail_dot)
        if len(self.trail_dots)>self.trail_dots.maxlen:
            old_dot=self.trail_dots.popleft()
            old_dot.remove()

    def draw_static(self):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0,self.maze.width)
        self.ax.set_ylim(self.maze.height,0)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self._draw_cell(x,y,self.maze.grid[y][x]==1)
        sx, sy = self.maze.start
        gx, gy = self.maze.goal
        self.ax.add_patch(patches.Circle((sx+0.5,sy+0.5),0.3,facecolor='#90be6d',alpha=0.3,edgecolor='#90be6d',linewidth=2))
        self.ax.add_patch(patches.Circle((gx+0.5,gy+0.5),0.3,facecolor='#f9c74f',alpha=0.3,edgecolor='#f9c74f',linewidth=2))
        self.ax.text(sx+0.5,sy+0.5,'START',ha='center',va='center',fontsize=10,fontweight='bold',color='#90be6d')
        self.ax.text(gx+0.5,gy+0.5,'GOAL',ha='center',va='center',fontsize=10,fontweight='bold',color='#f9c74f')
        self._draw_cheese()
        self.ax.set_xticks([]); self.ax.set_yticks([]); self.ax.set_frame_on(False)

    def animate(self,path,algorithm_name="Search Algorithm"):
        if not path:
            print("No path to animate!"); return
        self.draw_static(); self.current_frame=0
        title=self.ax.text(self.maze.width/2,-0.5,f"{algorithm_name} - Path Length: {len(path)}",ha='center',va='center',fontsize=14,fontweight='bold',color='white',transform=self.ax.transData)
        progress_text=self.ax.text(1,-0.5,"",fontsize=10,color='white',transform=self.ax.transData)
        def update(frame):
            self.current_frame=frame
            x,y=path[frame]
            direction=(x-path[frame-1][0],y-path[frame-1][1]) if frame>0 else (1,0)
            self._draw_path_line(path,frame)
            self._add_trail_dot(x,y,frame)
            self._draw_mouse(x,y,direction)
            progress_text.set_text(f"Step: {frame+1}/{len(path)} ({((frame+1)/len(path)*100):.0f}%)")
            return [self.path_line]+(self.mouse_artist or [])+[progress_text]
        anim=FuncAnimation(self.fig,update,frames=len(path),interval=5,repeat=False,blit=False)
        plt.tight_layout()
        try: 
            plt.get_current_fig_manager().window.state('zoomed') 
        except: 
            plt.get_current_fig_manager().resize(1000,800)
        plt.show()
        return anim